<?php

namespace App\Services;

use App\Models\Macuin\Autoparte;
use App\Models\Macuin\Carrito;
use App\Models\Macuin\CarritoLinea;
use App\Models\Macuin\Inventario;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class PortalCartService
{
    public const SESSION_UUID = 'macuin_carrito_uuid';

    public function currentCartForUser(int $laravelUserId): ?Carrito
    {
        $uuid = session(self::SESSION_UUID);
        if ($uuid) {
            $c = Carrito::query()->where('uuid', $uuid)->where('laravel_user_id', $laravelUserId)->first();
            if ($c) {
                return $c;
            }
            session()->forget(self::SESSION_UUID);
        }

        return Carrito::query()->where('laravel_user_id', $laravelUserId)->orderByDesc('id')->first();
    }

    public function getOrCreateCart(int $laravelUserId): Carrito
    {
        $cart = $this->currentCartForUser($laravelUserId);
        if ($cart) {
            return $cart;
        }
        $uuid = (string) Str::uuid();
        $cart = Carrito::query()->create([
            'uuid' => $uuid,
            'laravel_user_id' => $laravelUserId,
            'email_invitado' => null,
        ]);
        session([self::SESSION_UUID => $uuid]);

        return $cart;
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
        $ap = Autoparte::query()->with('inventario')->find($autoparteId);
        if (! $ap) {
            return ['ok' => false, 'message' => 'Producto no encontrado.'];
        }
        $stock = (int) ($ap->inventario?->stock_actual ?? 0);
        if ($stock < $cantidad) {
            return ['ok' => false, 'message' => 'Stock insuficiente para este producto.'];
        }
        $cart = $this->getOrCreateCart($laravelUserId);
        $precio = (float) $ap->precio_unitario;
        $existing = CarritoLinea::query()
            ->where('carrito_id', $cart->id)
            ->where('autoparte_id', $autoparteId)
            ->first();
        if ($existing) {
            $nueva = $existing->cantidad + $cantidad;
            if ($nueva > $stock) {
                return ['ok' => false, 'message' => 'No puedes superar el stock disponible ('.$stock.' unidades).'];
            }
            $existing->update(['cantidad' => $nueva]);

            return ['ok' => true, 'message' => 'Cantidad actualizada en el carrito.'];
        }
        CarritoLinea::query()->create([
            'carrito_id' => $cart->id,
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
        $line = CarritoLinea::query()->where('carrito_id', $cart->id)->where('id', $lineaId)->first();
        if (! $line) {
            return false;
        }
        $line->delete();

        return true;
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
        $line = CarritoLinea::query()->where('carrito_id', $cart->id)->where('id', $lineaId)->first();
        if (! $line) {
            return ['ok' => false, 'message' => 'Línea no encontrada.'];
        }
        $ap = Autoparte::query()->with('inventario')->find($line->autoparte_id);
        $stock = (int) ($ap?->inventario?->stock_actual ?? 0);
        if ($cantidad > $stock) {
            return ['ok' => false, 'message' => 'Stock insuficiente.'];
        }
        $line->update(['cantidad' => $cantidad]);

        return ['ok' => true, 'message' => 'Cantidad actualizada.'];
    }

    public function cartWithLines(int $laravelUserId): ?Carrito
    {
        $c = $this->currentCartForUser($laravelUserId);
        if (! $c) {
            return null;
        }
        $c->load(['lineas.autoparte.categoria', 'lineas.autoparte.marca', 'lineas.autoparte.inventario']);

        return $c;
    }

    public function lineCount(int $laravelUserId): int
    {
        $c = $this->currentCartForUser($laravelUserId);
        if (! $c) {
            return 0;
        }

        return (int) CarritoLinea::query()->where('carrito_id', $c->id)->sum('cantidad');
    }
}
