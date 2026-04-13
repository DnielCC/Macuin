<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreContactMessageRequest;
use App\Services\MacuinApiClient;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class ContactController extends Controller
{
    private MacuinApiClient $api;

    public function __construct(MacuinApiClient $api)
    {
        $this->api = $api;
    }

    public function create(): View
    {
        $mensajesContacto = collect();
        if (Auth::check()) {
            $user = Auth::user();
            $emailNorm = strtolower(trim((string) $user->email));

            // Fetch from API
            $mensajesFromApi = $this->api->get('/v1/portal-contacto/mensajes/por-email', ['email' => $emailNorm]) ?? [];
            
            // Limit 50 to match previous logic
            $mensajesContacto = collect($mensajesFromApi)
                ->map(fn($m) => (object)$m)
                ->take(50);
        }

        return view('contacto', [
            'mensajesContacto' => $mensajesContacto,
        ]);
    }

    public function store(StoreContactMessageRequest $request): RedirectResponse
    {
        $v = $request->validated();
        $phone = isset($v['phone']) ? trim((string) $v['phone']) : '';
        $phone = $phone === '' ? null : $phone;

        $this->api->post('/v1/portal-contacto/mensajes', [
            'email' => strtolower(trim($v['email'])),
            'name' => $v['name'],
            'phone' => $phone,
            'subject' => $v['subject'],
            'message' => $v['message']
        ]);

        return redirect()
            ->route('contacto')
            ->with('status', 'Mensaje enviado. Nuestro equipo lo verá en la bandeja de contacto. Te responderemos pronto.');
    }
}
