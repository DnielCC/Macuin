<?php

namespace App\Http\Controllers;

use App\Services\MacuinApiClient;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;
use Illuminate\Pagination\LengthAwarePaginator;

class CatalogController extends Controller
{
    private const ORDEN = ['nombre_asc', 'precio_asc', 'precio_desc', 'recientes'];

    private const VISTA = ['mosaico', 'lista'];

    private MacuinApiClient $api;

    public function __construct(MacuinApiClient $api)
    {
        $this->api = $api;
    }

    public function index(Request $request): View
    {
        $orden = $request->query('orden', 'nombre_asc');
        if (! in_array($orden, self::ORDEN, true)) {
            $orden = 'nombre_asc';
        }

        $vista = $request->query('vista', 'mosaico');
        if (! in_array($vista, self::VISTA, true)) {
            $vista = 'mosaico';
        }

        $stock = $request->query('stock', 'todos');
        if (! in_array($stock, ['todos', 'con'], true)) {
            $stock = 'todos';
        }

        $categoriaId = $request->filled('categoria_id') ? (int) $request->query('categoria_id') : null;
        $marcaId = $request->filled('marca_id') ? (int) $request->query('marca_id') : null;
        $qRaw = mb_strtolower(trim((string) $request->query('q', '')));

        try {
            // Caching static catalogs
            $categorias = Cache::remember('api_categorias_all', 120, function() {
                return collect($this->api->get('/v1/categorias') ?? []);
            });

            $marcas = Cache::remember('api_marcas_all', 120, function() {
                return collect($this->api->get('/v1/marcas') ?? []);
            });

            $inventarios = Cache::remember('api_inventarios_all', 30, function() {
                return collect($this->api->get('/v1/inventarios') ?? []);
            })->keyBy('autoparte_id');

            $autopartesData = Cache::remember('api_autopartes_all', 60, function() {
                return collect($this->api->get('/v1/autopartes') ?? []);
            });

            // Map standard object properties to mimic Elloquent behavior in views
            $autopartesRaw = $autopartesData->map(function ($ap) use ($categorias, $marcas, $inventarios) {
                // Attach relations manually
                $ap['categoria'] = $categorias->firstWhere('id', $ap['categoria_id']);
                $ap['marca'] = $marcas->firstWhere('id', $ap['marca_id']);
                $ap['inventario'] = $inventarios->get($ap['id']);
                
                // Keep it array or convert to object depending on view preference.
                // The current views use object notation like $producto->nombre, $producto->categoria->nombre.
                // So we'll cast deeply to objects.
                return json_decode(json_encode($ap), false);
            });

            // Filtering
            $filtered = $autopartesRaw->filter(function ($ap) use ($categoriaId, $marcaId, $stock, $qRaw) {
                if ($categoriaId && $ap->categoria_id !== $categoriaId) {
                    return false;
                }
                if ($marcaId && $ap->marca_id !== $marcaId) {
                    return false;
                }
                if ($stock === 'con') {
                    $stockAct = $ap->inventario->stock_actual ?? 0;
                    if ($stockAct <= 0) {
                        return false;
                    }
                }
                if ($qRaw !== '') {
                    $nombre = mb_strtolower($ap->nombre);
                    $sku = mb_strtolower($ap->sku_codigo);
                    if (!str_contains($nombre, $qRaw) && !str_contains($sku, $qRaw)) {
                        return false;
                    }
                }
                return true;
            });

            // Sorting
            $filtered = match ($orden) {
                'precio_asc' => $filtered->sortBy('precio_unitario'),
                'precio_desc' => $filtered->sortByDesc('precio_unitario'),
                'recientes' => $filtered->sortByDesc('fecha_alta')->sortByDesc('id'),
                default => $filtered->sortBy('nombre'),
            };

            // Pagination
            $page = filter_var($request->query('page', 1), FILTER_VALIDATE_INT) ?: 1;
            $perPage = 24;
            $paginated = new LengthAwarePaginator(
                $filtered->forPage($page, $perPage)->values(), // Items on current page
                $filtered->count(), // Total items
                $perPage,
                $page,
                ['path' => $request->url(), 'query' => $request->query()]
            );

        } catch (\Throwable $e) {
            report($e);
            $categorias = collect();
            $marcas = collect();
            $paginated = new LengthAwarePaginator([], 0, 24, 1);
        }

        return view('catalogo', [
            'categorias' => $categorias->map(fn($c) => (object)$c),
            'marcas' => $marcas->map(fn($m) => (object)$m),
            'productos' => $paginated,
            'orden' => $orden,
            'vista' => $vista,
            'stock' => $stock,
            'categoriaId' => $categoriaId,
            'marcaId' => $marcaId,
            'qRaw' => $qRaw,
        ]);
    }
}
