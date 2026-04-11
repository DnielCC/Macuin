<?php

namespace App\Http\Controllers;

use App\Http\Requests\AddCartLineRequest;
use App\Http\Requests\UpdateCartLineRequest;
use App\Services\PortalCartService;
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
        if ($cart) {
            foreach ($cart->lineas as $ln) {
                $subtotal += (float) $ln->precio_unitario * (int) $ln->cantidad;
            }
        }

        return view('carrito', [
            'carrito' => $cart,
            'subtotal' => $subtotal,
            'envio' => $envio,
            'total' => $subtotal + ($cart && $cart->lineas->isNotEmpty() ? $envio : 0),
        ]);
    }

    public function add(AddCartLineRequest $request): RedirectResponse
    {
        $r = $this->cart->addLine(
            (int) $request->user()->id,
            (int) $request->validated('autoparte_id'),
            (int) $request->validated('cantidad')
        );

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
