<?php

namespace App\Services;

use App\Models\Macuin\CarritoLinea;
use App\Models\Macuin\Cliente;
use App\Models\Macuin\DetallePedido;
use App\Models\Macuin\Direccion;
use App\Models\Macuin\EstatusPedido;
use App\Models\Macuin\Pago;
use App\Models\Macuin\Pedido;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use RuntimeException;
use Throwable;

class CheckoutService
{
    public function __construct(
        protected PortalCartService $cart,
        protected PortalUsuarioResolver $actor,
    ) {}

    /**
     * @param  array<string, string>  $direccion  calle, num_ext, colonia, municipio, estado, cp, num_int?, referencias?
     * @return array{ok: bool, message: string, pedido_id?: int, pago_id?: int}
     */
    public function procesar(User $user, array $direccion, string $titularTarjeta, string $numeroTarjeta): array
    {
        $cart = $this->cart->cartWithLines((int) $user->id);
        if (! $cart || $cart->lineas->isEmpty()) {
            return ['ok' => false, 'message' => 'Tu carrito está vacío.'];
        }

        $sim = $this->simularPasarela($numeroTarjeta, $titularTarjeta);
        if (! $sim['aprobado']) {
            return ['ok' => false, 'message' => $sim['mensaje']];
        }

        $estatus = EstatusPedido::query()->where('nombre', 'Pendiente')->first();
        if (! $estatus) {
            return ['ok' => false, 'message' => 'No existe el estatus «Pendiente» en la base de datos. Ejecuta el seed de la API.'];
        }

        try {
            $actorId = $this->actor->internalUserId();
        } catch (RuntimeException $e) {
            return ['ok' => false, 'message' => $e->getMessage()];
        }

        $subtotal = 0.0;
        foreach ($cart->lineas as $ln) {
            $subtotal += (float) $ln->precio_unitario * (int) $ln->cantidad;
        }
        $envio = (float) config('macuin.envio_fijo_mxn', 150);
        $total = round($subtotal + $envio, 2);

        try {
            DB::beginTransaction();

            $cliente = Cliente::query()->firstOrCreate(
                ['email' => strtolower(trim($user->email))],
                [
                    'nombre' => $user->name,
                    'telefono' => $user->phone,
                    'activo' => true,
                    'notas' => 'Portal Laravel — user_id '.$user->id,
                ]
            );

            $dir = Direccion::query()->create([
                'calle_principal' => $direccion['calle_principal'],
                'num_ext' => $direccion['num_ext'],
                'num_int' => $direccion['num_int'] ?? null,
                'colonia' => $direccion['colonia'],
                'municipio' => $direccion['municipio'],
                'estado' => $direccion['estado'],
                'cp' => $direccion['cp'],
                'referencias' => $direccion['referencias'] ?? null,
                'cliente_id' => $cliente->id,
            ]);

            $pedido = Pedido::query()->create([
                'folio' => 'WEB-'.now()->format('YmdHis').'-'.$user->id,
                'usuario_id' => $actorId,
                'estatus_id' => $estatus->id,
                'total' => $total,
                'direccion_envio_id' => $dir->id,
                'cliente_id' => $cliente->id,
            ]);

            foreach ($cart->lineas as $ln) {
                DetallePedido::query()->create([
                    'pedido_id' => $pedido->id,
                    'autoparte_id' => $ln->autoparte_id,
                    'cantidad' => $ln->cantidad,
                    'precio_historico' => $ln->precio_unitario,
                ]);
            }

            $pago = Pago::query()->create([
                'pedido_id' => $pedido->id,
                'carrito_id' => null,
                'monto' => $total,
                'moneda' => 'MXN',
                'estado' => 'aprobado',
                'pasarela' => config('macuin.pasarela_nombre'),
                'referencia_externa' => $sim['referencia'],
                'respuesta_proveedor' => json_encode($sim['detalle'], JSON_UNESCAPED_UNICODE),
            ]);

            CarritoLinea::query()->where('carrito_id', $cart->id)->delete();
            $cart->delete();
            $this->cart->forgetSessionCart();

            DB::commit();

            return [
                'ok' => true,
                'message' => 'Pago aprobado y pedido registrado.',
                'pedido_id' => $pedido->id,
                'pago_id' => $pago->id,
            ];
        } catch (Throwable $e) {
            DB::rollBack();
            report($e);

            return ['ok' => false, 'message' => 'No se pudo completar el pedido. Intenta de nuevo o contacta soporte.'];
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
