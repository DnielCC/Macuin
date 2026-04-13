<?php

namespace App\Http\Controllers;

use App\Services\MacuinApiClient;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PedidosController extends Controller
{
    private MacuinApiClient $api;

    public function __construct(MacuinApiClient $api)
    {
        $this->api = $api;
    }

    public function index(Request $request): View
    {
        $pedidosInfo = collect();
        $email = mb_strtolower(trim((string) $request->user()->email));

        $cliente = $this->api->get('/v1/clientes/por-email', ['email' => $email]);

        if ($cliente) {
            $todosLosPedidos = $this->api->get('/v1/pedidos') ?? [];
            // Filtramos los pedidos del cliente
            $pedidosCliente = collect($todosLosPedidos)->filter(function ($p) use ($cliente) {
                return $p['cliente_id'] === $cliente['id'];
            })->sortByDesc('id')->take(100);

            // Fetch estatus para asociar el nombre
            $estatusList = $this->api->get('/v1/estatus-pedido') ?? [];
            $estatusMap = collect($estatusList)->keyBy('id');

            $pedidosInfo = $pedidosCliente->map(function ($p) use ($estatusMap) {
                $p['estatus'] = $estatusMap->get($p['estatus_id']);
                return json_decode(json_encode($p), false); // cast to object for view
            });
        }

        return view('pedidos', ['pedidos' => $pedidosInfo]);
    }
}
