<?php

namespace App\Http\Controllers;

use App\Services\MacuinApiClient;
use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;

class HomeController extends Controller
{
    private MacuinApiClient $api;

    public function __construct(MacuinApiClient $api)
    {
        $this->api = $api;
    }

    public function index(): View
    {
        try {
            $categorias = Cache::remember('api_categorias_all', 120, function() {
                return collect($this->api->get('/v1/categorias') ?? []);
            });

            $autopartes = Cache::remember('api_autopartes_all', 60, function() {
                return collect($this->api->get('/v1/autopartes') ?? []);
            });

            // Count autopartes per category
            $counts = $autopartes->countBy('categoria_id');

            $categoriasDestacadas = $categorias->map(function ($c) use ($counts) {
                $c['autopartes_count'] = $counts->get($c['id'], 0);
                return (object)$c;
            })
            ->sortByDesc('autopartes_count')
            ->values()
            ->take(8);

        } catch (\Throwable $e) {
            report($e);
            $categoriasDestacadas = collect();
        }

        return view('home', [
            'categoriasDestacadas' => $categoriasDestacadas,
        ]);
    }
}
