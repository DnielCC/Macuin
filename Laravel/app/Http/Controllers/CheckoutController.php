<?php

namespace App\Http\Controllers;

use App\Http\Requests\CheckoutPagoRequest;
use App\Services\CheckoutService;
use App\Services\PortalCartService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class CheckoutController extends Controller
{
    public function __construct(
        protected PortalCartService $cart,
        protected CheckoutService $checkout,
    ) {}

    public function show(Request $request): View|RedirectResponse
    {
        if (! $request->user()) {
            return redirect()->route('login')->with('error', 'Inicia sesión para pagar.');
        }
        $cart = $this->cart->cartWithLines((int) $request->user()->id);
        if (! $cart || empty($cart['lineas'])) {
            return redirect()->route('carrito')->with('error', 'Tu carrito está vacío.');
        }
        $subtotal = 0.0;
        foreach ($cart['lineas'] as $ln) {
            $subtotal += (float) $ln['precio_unitario'] * (int) $ln['cantidad'];
        }
        $envio = (float) config('macuin.envio_fijo_mxn', 150);

        // Convert for view
        $carritoView = (object) [
            'id' => $cart['id'],
            'uuid' => $cart['uuid'],
            'lineas' => collect($cart['lineas'])->map(function ($ln) {
                return json_decode(json_encode($ln), false); // cast deep to object
            })
        ];

        return view('pago', [
            'carrito' => $carritoView,
            'subtotal' => $subtotal,
            'envio' => $envio,
            'total' => $subtotal + $envio,
            'estadosMexico' => config('estados_mexico', []),
        ]);
    }

    public function procesar(CheckoutPagoRequest $request): RedirectResponse
    {
        $v = $request->validated();
        $dir = [
            'calle_principal' => $v['calle_principal'],
            'num_ext' => $v['num_ext'],
            'num_int' => $v['num_int'] ?? null,
            'colonia' => $v['colonia'],
            'municipio' => $v['municipio'],
            'estado' => $v['estado'],
            'cp' => $v['cp'],
            'referencias' => $v['referencias'] ?? null,
        ];

        usleep(400000);

        $r = $this->checkout->procesar(
            $request->user(),
            $dir,
            $v['titular_tarjeta'],
            $v['numero_tarjeta']
        );

        if (! $r['ok']) {
            return back()->withInput()->with('error', $r['message']);
        }

        return redirect()
            ->route('pedidos')
            ->with('status', $r['message'].' Pedido #'.($r['pedido_id'] ?? '?').'.');
    }
}
