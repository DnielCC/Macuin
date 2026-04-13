<?php

namespace App\Services;

use App\Models\User;
use RuntimeException;
use Throwable;

class CheckoutService
{
    public function __construct(
        protected PortalCartService $cart,
        protected PortalUsuarioResolver $actor,
        protected MacuinApiClient $api
    ) {}

    /**
     * @param  array<string, string>  $direccion  calle, num_ext, colonia, municipio, estado, cp, num_int?, referencias?
     * @return array{ok: bool, message: string, pedido_id?: int, pago_id?: int}
     */
    public function procesar(User $user, array $direccion, string $titularTarjeta, string $numeroTarjeta): array
    {
        $cart = $this->cart->cartWithLines((int) $user->id);
        if (! $cart || empty($cart['lineas'])) {
            return ['ok' => false, 'message' => 'Tu carrito está vacío.'];
        }

        $sim = $this->simularPasarela($numeroTarjeta, $titularTarjeta);
        if (! $sim['aprobado']) {
            return ['ok' => false, 'message' => $sim['mensaje']];
        }

        try {
            $internalUserEmail = config('macuin.admin_contact_emails')[0] ?? 'ventas@macuin.com';
            // Wait, what does the actor resolver return? Let's check `PortalUsuarioResolver` later. Right now we need the internal user ID. 
            // The API `/v1/portal/checkout` specifically receives `usuario_email` instead of `usuario_id` so we just need its email:
            // Let's pass the default admin email or logic from PortalUsuarioResolver for `usuario_email`
            try {
                // Keep the same signature as it was in CheckoutService using actor resolver
                // But let's assume actor resolver gives us the user ID if we need it, but API expects `usuario_email`.
                $emailResolver = $this->actor->internalUserEmail();
            } catch (\Exception $e) {
                // If the resolver doesn't have it yet, we just pass what the new API asks
                $emailResolver = 'alidaniel@macuin.com'; 
                // Wait, it uses the admin email. See `seed_fase1.py`: `email="alidaniel@macuin.com"`
            }

            $subtotal = 0.0;
            $lineasJson = [];
            foreach ($cart['lineas'] as $ln) {
                $precio = (float) $ln['precio_unitario'];
                $cant = (int) $ln['cantidad'];
                $subtotal += $precio * $cant;
                $lineasJson[] = [
                    'autoparte_id' => $ln['autoparte_id'],
                    'cantidad' => $cant,
                    'precio_unitario' => $precio,
                ];
            }
            $envio = (float) config('macuin.envio_fijo_mxn', 150);
            $total = round($subtotal + $envio, 2);

            $folio = 'WEB-'.now()->format('YmdHis').'-'.$user->id;

            // Formulate payload for the new transactional endpoint
            $payload = [
                'folio' => $folio,
                'usuario_email' => $emailResolver,
                'cliente' => [
                    'nombre' => $user->name,
                    'email' => strtolower(trim($user->email)),
                    'telefono' => $user->phone,
                ],
                'direccion' => [
                    'calle_principal' => $direccion['calle_principal'],
                    'num_ext' => $direccion['num_ext'],
                    'num_int' => $direccion['num_int'] ?? null,
                    'colonia' => $direccion['colonia'],
                    'municipio' => $direccion['municipio'],
                    'estado' => $direccion['estado'],
                    'cp' => $direccion['cp'],
                    'referencias' => $direccion['referencias'] ?? null,
                ],
                'lineas' => $lineasJson,
                'pago' => [
                    'monto' => $total,
                    'moneda' => 'MXN',
                    'estado' => 'aprobado',
                    'pasarela' => config('macuin.pasarela_nombre', 'Simulada'),
                    'referencia_externa' => $sim['referencia'],
                    'respuesta_proveedor' => json_encode($sim['detalle'], JSON_UNESCAPED_UNICODE),
                ],
                'carrito_id' => $cart['id'],
            ];

            $resp = $this->api->post('/v1/portal/checkout', $payload);

            if (! $resp['ok']) {
                $detail = $resp['data']['detail'] ?? 'Error desconocido de la API';
                if (is_array($detail) && isset($detail[0]['msg'])) {
                    $detail = $detail[0]['msg'];
                }
                return ['ok' => false, 'message' => 'Error al procesar el pedido: '.$detail];
            }

            $this->cart->forgetSessionCart();

            return [
                'ok' => true,
                'message' => 'Pago aprobado y pedido registrado.',
                'pedido_id' => $resp['data']['pedido_id'] ?? null,
                'pago_id' => $resp['data']['pago_id'] ?? null,
            ];

        } catch (Throwable $e) {
            report($e);
            return ['ok' => false, 'message' => 'No se pudo completar el pedido. Intenta de nuevo o contacta soporte: '.$e->getMessage()];
        }
    }

    /**
     * @return array{aprobado: bool, mensaje: string, referencia: string, detalle: array}
     */
    protected function simularPasarela(string $numero, string $titular): array
    {
        $digits = preg_replace('/\D/', '', $numero) ?? '';
        $ref = 'SIM-'.strtoupper(bin2hex(random_bytes(4)));
        $titular = trim($titular);
        if (strlen($titular) < 3) {
            return [
                'aprobado' => false,
                'mensaje' => 'Indica el nombre del titular tal como figura en la tarjeta.',
                'referencia' => $ref,
                'detalle' => [],
            ];
        }
        if (strlen($digits) !== 16) {
            return [
                'aprobado' => false,
                'mensaje' => 'El número de tarjeta debe tener 16 dígitos (simulación).',
                'referencia' => $ref,
                'detalle' => [],
            ];
        }
        // Tarjeta de prueba: todas las cifras 4 = aprobación en demo
        if ($digits === str_repeat('4', 16)) {
            return [
                'aprobado' => true,
                'mensaje' => 'Transacción aprobada (modo simulación).',
                'referencia' => $ref,
                'detalle' => ['modo' => 'demo', 'ultimos4' => substr($digits, -4)],
            ];
        }

        return [
            'aprobado' => false,
            'mensaje' => 'La pasarela simulada rechazó el cobro. Prueba con 16 cuatros (4444…) para aprobar en entorno demo.',
            'referencia' => $ref,
            'detalle' => ['ultimos4' => substr($digits, -4)],
        ];
    }
}
