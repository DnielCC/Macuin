<?php

namespace App\Http\Controllers;

use App\Models\Macuin\Cliente;
use App\Models\Macuin\Pedido;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PedidosController extends Controller
{
    public function index(Request $request): View
    {
        $pedidos = collect();
        $email = strtolower(trim((string) $request->user()->email));
        $cliente = Cliente::query()->whereRaw('LOWER(email) = ?', [$email])->first();
        if ($cliente) {
            $pedidos = Pedido::query()
                ->where('cliente_id', $cliente->id)
                ->with('estatus')
                ->orderByDesc('id')
                ->limit(100)
                ->get();
        }

        return view('pedidos', ['pedidos' => $pedidos]);
    }
}
