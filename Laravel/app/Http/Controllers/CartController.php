<?php

namespace App\Http\Controllers;

use App\Http\Requests\AddCartLineRequest;
use App\Http\Requests\UpdateCartLineRequest;
use App\Services\PortalCartService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class CartController extends Controller
{
    public function __construct(
        protected PortalCartService $cart,
    ) {}

    public function index(Request $request): View|RedirectResponse
    {
        if (! $request->user()) {
            return redirect()->route('login')->with('error', 'Inicia sesión para ver tu carrito.');
        }
        $cart = $this->cart->cartWithLines((int) $request->user()->id);
        $envio = (float) config('macuin.envio_fijo_mxn', 150);
        $subtotal = 0.0;
        if ($cart && !empty($cart['lineas'])) {
            foreach ($cart['lineas'] as $ln) {
                $subtotal += (float) $ln['precio_unitario'] * (int) $ln['cantidad'];
            }
        }

        // We convert it to an object so the blade view ($carrito->lineas) doesn't break.
        $carritoView = null;
        if ($cart) {
            $carritoView = (object) [
                'id' => $cart['id'],
                'uuid' => $cart['uuid'],
                'lineas' => collect($cart['lineas'] ?? [])->map(function ($ln) {
                    return json_decode(json_encode($ln), false); // cast deep to object
                })
            ];
        }

        return view('carrito', [
            'carrito' => $carritoView,
            'subtotal' => $subtotal,
            'envio' => $envio,
            'total' => $subtotal + ($carritoView && $carritoView->lineas->isNotEmpty() ? $envio : 0),
        ]);
    }

    public function add(AddCartLineRequest $request): RedirectResponse|JsonResponse
    {
        $r = $this->cart->addLine(
            (int) $request->user()->id,
            (int) $request->validated('autoparte_id'),
            (int) $request->validated('cantidad')
        );

        if ($request->ajax() || $request->wantsJson()) {
            $count = $this->cart->lineCount((int) $request->user()->id);

            return response()->json([
                'ok' => $r['ok'],
                'message' => $r['message'],
                'cart_count' => $count,
            ], $r['ok'] ? 200 : 422);
        }

        return redirect()
            ->route('carrito')
            ->with($r['ok'] ? 'status' : 'error', $r['message']);
    }

    public function remove(Request $request, int $linea): RedirectResponse
    {
        $ok = $this->cart->removeLine((int) $request->user()->id, $linea);

        return redirect()
            ->route('carrito')
            ->with($ok ? 'status' : 'error', $ok ? 'Producto quitado del carrito.' : 'No se pudo quitar la línea.');
    }

    public function updateQty(UpdateCartLineRequest $request, int $linea): RedirectResponse
    {
        $r = $this->cart->updateLineQty(
            (int) $request->user()->id,
            $linea,
            (int) $request->validated('cantidad')
        );

        return redirect()
            ->route('carrito')
            ->with($r['ok'] ? 'status' : 'error', $r['message']);
    }
}
