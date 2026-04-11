<?php

namespace App\Http\Controllers;

use App\Models\Macuin\Autoparte;
use App\Models\Macuin\Categoria;
use App\Models\Macuin\Marca;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Schema;
use Illuminate\View\View;

class CatalogController extends Controller
{
    private const ORDEN = ['nombre_asc', 'precio_asc', 'precio_desc', 'recientes'];

    private const VISTA = ['mosaico', 'lista'];

    public function index(Request $request): View
    {
        $categorias = collect();
        $marcas = collect();
        $productos = collect();

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
        $qRaw = trim((string) $request->query('q', ''));

        try {
            if (! Schema::hasTable('autopartes')) {
                return view('catalogo', [
                    'categorias' => $categorias,
                    'marcas' => $marcas,
                    'productos' => $productos,
                    'orden' => $orden,
                    'vista' => $vista,
                    'stock' => $stock,
                    'categoriaId' => $categoriaId,
                    'marcaId' => $marcaId,
                    'qRaw' => $qRaw,
                ]);
            }

            $categorias = Categoria::query()->orderBy('nombre')->get();
            if (Schema::hasTable('marcas')) {
                $marcas = Marca::query()->orderBy('nombre')->get();
            }

            $query = Autoparte::query()
                ->with(['categoria', 'marca', 'inventario']);

            if ($categoriaId) {
                $query->where('categoria_id', $categoriaId);
            }
            if ($marcaId) {
                $query->where('marca_id', $marcaId);
            }
            if ($stock === 'con') {
                $query->whereHas('inventario', function ($w) {
                    $w->where('stock_actual', '>', 0);
                });
            }

            $this->applySearch($query, $qRaw);

            match ($orden) {
                'precio_asc' => $query->orderBy('precio_unitario'),
                'precio_desc' => $query->orderByDesc('precio_unitario'),
                'recientes' => $query->orderByDesc('fecha_alta')->orderByDesc('id'),
                default => $query->orderBy('nombre'),
            };

            $productos = $query->paginate(24)->withQueryString();
        } catch (\Throwable $e) {
            report($e);
        }

        return view('catalogo', [
            'categorias' => $categorias,
            'marcas' => $marcas,
            'productos' => $productos,
            'orden' => $orden,
            'vista' => $vista,
            'stock' => $stock,
            'categoriaId' => $categoriaId,
            'marcaId' => $marcaId,
            'qRaw' => $qRaw,
        ]);
    }

    /**
     * @param  \Illuminate\Database\Eloquent\Builder<Autoparte>  $query
     */
    private function applySearch($query, string $qRaw): void
    {
        if ($qRaw === '') {
            return;
        }

        $term = '%'.str_replace(['%', '_'], ['\\%', '\\_'], $qRaw).'%';
        $driver = Schema::getConnection()->getDriverName();

        $query->where(function ($w) use ($term, $driver) {
            if ($driver === 'pgsql') {
                $w->where('nombre', 'ilike', $term)
                    ->orWhere('sku_codigo', 'ilike', $term);
            } else {
                $w->where('nombre', 'like', $term)
                    ->orWhere('sku_codigo', 'like', $term);
            }
        });
    }
}
