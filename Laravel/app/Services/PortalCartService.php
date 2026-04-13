<?php

namespace App\Services;

use Illuminate\Support\Str;

class PortalCartService
{
    public const SESSION_UUID = 'macuin_carrito_uuid';

    private MacuinApiClient $api;

    public function __construct(MacuinApiClient $api)
    {
        $this->api = $api;
    }

    public function currentCartForUser(int $laravelUserId): ?array
    {
        $cart = $this->api->get('/v1/carritos/por-usuario/'.$laravelUserId);
        if ($cart) {
            session([self::SESSION_UUID => $cart['uuid']]);
        } else {
            session()->forget(self::SESSION_UUID);
        }
        return $cart;
    }

    public function getOrCreateCart(int $laravelUserId): array
    {
        $cart = $this->currentCartForUser($laravelUserId);
        if ($cart) {
            return $cart;
        }

        $uuid = (string) Str::uuid();
        $resp = $this->api->post('/v1/carritos/', [
            'uuid' => $uuid,
            'laravel_user_id' => $laravelUserId,
            'email_invitado' => null,
        ]);

        if ($resp['ok'] && $resp['data']) {
            session([self::SESSION_UUID => $resp['data']['uuid']]);
            // Return empty structure as expected for a new cart
            return ['id' => $resp['data']['id'], 'uuid' => $uuid, 'lineas' => []];
        }

        throw new \Exception('No se pudo crear el carrito en la API');
    }

    public function forgetSessionCart(): void
    {
        session()->forget(self::SESSION_UUID);
    }

    /**
     * @return array{ok: bool, message: string}
     */
    public function addLine(int $laravelUserId, int $autoparteId, int $cantidad): array
    {
        if ($cantidad < 1 || $cantidad > 999) {
            return ['ok' => false, 'message' => 'La cantidad debe estar entre 1 y 999.'];
        }

        $ap = $this->api->get('/v1/autopartes/'.$autoparteId);
        if (! $ap) {
            return ['ok' => false, 'message' => 'Producto no encontrado.'];
        }

        // Get inventory stock
        $inventarios = $this->api->get('/v1/inventarios', [], 5) ?? [];
        $stock = 0;
        foreach ($inventarios as $inv) {
            if ($inv['autoparte_id'] === $autoparteId) {
                $stock = (int) $inv['stock_actual'];
                break;
            }
        }

        if ($stock < $cantidad) {
            return ['ok' => false, 'message' => 'Stock insuficiente para este producto.'];
        }

        $cart = $this->getOrCreateCart($laravelUserId);
        $precio = (float) $ap['precio_unitario'];

        // Check if line exists
        $lineas = $cart['lineas'] ?? [];
        $existingLineId = null;
        $existingQty = 0;
        foreach ($lineas as $ln) {
            if ($ln['autoparte_id'] === $autoparteId) {
                $existingLineId = $ln['id'];
                $existingQty = $ln['cantidad'];
                break;
            }
        }

        if ($existingLineId) {
            $nueva = $existingQty + $cantidad;
            if ($nueva > $stock) {
                return ['ok' => false, 'message' => 'No puedes superar el stock disponible ('.$stock.' unidades).'];
            }
            $this->api->patch("/v1/carritos/{$cart['id']}/lineas/{$existingLineId}", [
                'cantidad' => $nueva
            ]); // Using our specific signature or API structure (Wait, API expects query param 'cantidad' currently)
            // Wait, our new PATCH method in carritos.py expects ?cantidad=X query param:
            $this->api->patch("/v1/carritos/{$cart['id']}/lineas/{$existingLineId}?cantidad={$nueva}");
            return ['ok' => true, 'message' => 'Cantidad actualizada en el carrito.'];
        }

        $this->api->post("/v1/carritos/{$cart['id']}/lineas", [
            'autoparte_id' => $autoparteId,
            'cantidad' => $cantidad,
            'precio_unitario' => $precio,
        ]);

        return ['ok' => true, 'message' => 'Producto agregado al carrito.'];
    }

    public function removeLine(int $laravelUserId, int $lineaId): bool
    {
        $cart = $this->currentCartForUser($laravelUserId);
        if (! $cart) {
            return false;
        }

        $resp = $this->api->delete("/v1/carritos/{$cart['id']}/lineas/{$lineaId}");
        return $resp['ok'];
    }

    public function updateLineQty(int $laravelUserId, int $lineaId, int $cantidad): array
    {
        if ($cantidad < 1 || $cantidad > 999) {
            return ['ok' => false, 'message' => 'Cantidad inválida.'];
        }
        $cart = $this->currentCartForUser($laravelUserId);
        if (! $cart) {
            return ['ok' => false, 'message' => 'Carrito no encontrado.'];
        }

        $lineaEncontrada = null;
        foreach (($cart['lineas'] ?? []) as $ln) {
            if ($ln['id'] === $lineaId) {
                $lineaEncontrada = $ln;
                break;
            }
        }

        if (! $lineaEncontrada) {
            return ['ok' => false, 'message' => 'Línea no encontrada.'];
        }

        $stock = (int) ($lineaEncontrada['autoparte']['inventario']['stock_actual'] ?? 0);
        if ($cantidad > $stock) {
            return ['ok' => false, 'message' => 'Stock insuficiente.'];
        }

        // Send query param as that's what we built in carritos.py: PATCH /{carrito_id}/lineas/{linea_id}?cantidad=x
        $resp = $this->api->patch("/v1/carritos/{$cart['id']}/lineas/{$lineaId}?cantidad={$cantidad}");

        return $resp['ok'] 
            ? ['ok' => true, 'message' => 'Cantidad actualizada.']
            : ['ok' => false, 'message' => 'Error al actualizar cantidad.'];
    }

    public function cartWithLines(int $laravelUserId): ?array
    {
        return $this->currentCartForUser($laravelUserId);
    }

    public function lineCount(int $laravelUserId): int
    {
        $c = $this->currentCartForUser($laravelUserId);
        if (! $c) {
            return 0;
        }

        $count = 0;
        foreach (($c['lineas'] ?? []) as $ln) {
            $count += (int) $ln['cantidad'];
        }
        return $count;
    }
}

