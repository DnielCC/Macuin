<?php

namespace App\Http\Controllers;

use App\Services\MacuinApiClient;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class ContactInboxController extends Controller
{
    private MacuinApiClient $api;

    public function __construct(MacuinApiClient $api)
    {
        $this->api = $api;
    }

    public function index(): View
    {
        $mensajes = $this->api->get('/v1/portal-contacto/mensajes') ?? [];
        $mensajes = collect($mensajes)->map(fn($m) => (object)$m);

        $noLeidos = $this->api->get('/v1/portal-contacto/mensajes/no-leidos/count');
        $sinLeerCount = $noLeidos['count'] ?? 0;

        return view('admin.contacto-inbox', [
            'mensajes' => $mensajes,
            'sinLeer' => $sinLeerCount,
        ]);
    }

    public function marcarLeido(Request $request, int $mensaje): RedirectResponse
    {
        $this->api->patch("/v1/portal-contacto/mensajes/{$mensaje}/leido");

        return redirect()->route('admin.contacto.inbox')->with('status', 'Mensaje marcado como leído.');
    }

    public function responder(Request $request, int $mensaje): RedirectResponse
    {
        $field = 'reply_'.$mensaje;
        $data = $request->validate(
            [
                $field => ['required', 'string', 'min:1', 'max:5000'],
            ],
            [
                $field.'.required' => 'Escribe una respuesta o nota para el cliente.',
            ]
        );

        $this->api->patch("/v1/portal-contacto/mensajes/{$mensaje}/responder", [
            'admin_reply' => $data[$field]
        ]);

        return redirect()
            ->route('admin.contacto.inbox')
            ->with('status', 'Respuesta guardada. Puedes enviarla al correo del cliente con el enlace «Abrir correo».');
    }
}
