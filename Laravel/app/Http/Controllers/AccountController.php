<?php

namespace App\Http\Controllers;

use App\Services\MacuinApiClient;
use Illuminate\View\View;

class AccountController extends Controller
{
    private MacuinApiClient $api;

    public function __construct(MacuinApiClient $api)
    {
        $this->api = $api;
    }

    public function show(): View
    {
        $user = auth()->user();
        $emailNorm = strtolower(trim((string) $user->email));

        // Fetch from API
        $mensajesFromApi = $this->api->get('/v1/portal-contacto/mensajes/por-email', ['email' => $emailNorm]) ?? [];
        
        // Limit 50 to match previous logic
        $mensajesContacto = collect($mensajesFromApi)
            ->map(fn($m) => (object)$m)
            ->take(50);

        return view('auth.account', [
            'mensajesContacto' => $mensajesContacto,
        ]);
    }
}
