<?php

namespace App\Http\Controllers;

use App\Services\MacuinApiClient;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PedidosController extends Controller
{
    private MacuinApiClient $api;

    /** Estatus que no admiten cancelación (misma lógica que Flask admin). */
    private const ESTATUS_NO_CANCELABLES = ['Enviado', 'Entregado', 'Cancelado'];

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

    /**
     * Cancelar un pedido del cliente autenticado.
     *
     * Valida que el pedido pertenezca al cliente, que no esté ya cancelado
     * y que su estatus no sea terminal (Enviado / Entregado / Cancelado).
     * Usa el endpoint PATCH /v1/pedidos/{id}/cancelar de la API — el mismo
     * que utiliza el panel Flask.
     */
    public function cancelar(Request $request, int $pedido): RedirectResponse
    {
        $request->validate([
            'motivo_cancelacion' => ['required', 'string', 'min:3', 'max:2000'],
        ], [
            'motivo_cancelacion.required' => 'Debes indicar un motivo de cancelación.',
            'motivo_cancelacion.min' => 'El motivo debe tener al menos 3 caracteres.',
        ]);

        $email = mb_strtolower(trim((string) $request->user()->email));
        $cliente = $this->api->get('/v1/clientes/por-email', ['email' => $email]);

        if (! $cliente) {
            return back()->with('error', 'No se encontró tu cuenta de cliente.');
        }

        // Obtener el pedido y verificar propiedad
        $pedidoData = $this->api->get("/v1/pedidos/{$pedido}");

        if (! $pedidoData || ($pedidoData['cliente_id'] ?? null) !== $cliente['id']) {
            return back()->with('error', 'Pedido no encontrado o no te pertenece.');
        }

        // Verificar que no esté ya cancelado
        if (! empty($pedidoData['motivo_cancelacion'])) {
            return back()->with('error', 'Este pedido ya fue cancelado anteriormente.');
        }

        // Verificar estatus que no admite cancelación
        $estatusList = $this->api->get('/v1/estatus-pedido') ?? [];
        $estatusMap = collect($estatusList)->keyBy('id');
        $estatusActual = $estatusMap->get($pedidoData['estatus_id']);
        $nombreEstatus = $estatusActual['nombre'] ?? '';

        if (in_array($nombreEstatus, self::ESTATUS_NO_CANCELABLES, true)) {
            return back()->with('error', "No se puede cancelar un pedido con estatus «{$nombreEstatus}».");
        }

        // Llamar al endpoint de cancelación de la API
        $result = $this->api->patch("/v1/pedidos/{$pedido}/cancelar", [
            'motivo_cancelacion' => $request->input('motivo_cancelacion'),
        ]);

        if (! $result['ok']) {
            return back()->with('error', 'No se pudo cancelar el pedido. Intenta de nuevo.');
        }

        return back()->with('status', "Pedido #{$pedido} cancelado correctamente.");
    }
}
