<?php

namespace App\Http\Controllers;

use App\Models\Macuin\Categoria;
use Illuminate\Support\Facades\Schema;
use Illuminate\View\View;

class HomeController extends Controller
{
    public function index(): View
    {
        $categoriasDestacadas = collect();
        try {
            if (Schema::hasTable('categorias')) {
                $categoriasDestacadas = Categoria::query()
                    ->withCount('autopartes')
                    ->orderByDesc('autopartes_count')
                    ->orderBy('nombre')
                    ->limit(8)
                    ->get();
            }
        } catch (\Throwable $e) {
            report($e);
        }

        return view('home', [
            'categoriasDestacadas' => $categoriasDestacadas,
        ]);
    }
}
