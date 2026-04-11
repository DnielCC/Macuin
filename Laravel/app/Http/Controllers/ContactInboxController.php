<?php

namespace App\Http\Controllers;

use App\Models\ContactMessage;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class ContactInboxController extends Controller
{
    public function index(): View
    {
        $mensajes = ContactMessage::query()
            ->orderByDesc('id')
            ->limit(200)
            ->get();

        return view('admin.contacto-inbox', [
            'mensajes' => $mensajes,
            'sinLeer' => ContactMessage::query()->where('is_read', false)->count(),
        ]);
    }

    public function marcarLeido(Request $request, ContactMessage $mensaje): RedirectResponse
    {
        $mensaje->update([
            'is_read' => true,
            'read_at' => now(),
        ]);

        return redirect()->route('admin.contacto.inbox')->with('status', 'Mensaje marcado como leído.');
    }

    public function responder(Request $request, ContactMessage $mensaje): RedirectResponse
    {
        $field = 'reply_'.$mensaje->id;
        $data = $request->validate(
            [
                $field => ['required', 'string', 'min:1', 'max:5000'],
            ],
            [
                $field.'.required' => 'Escribe una respuesta o nota para el cliente.',
            ]
        );

        $mensaje->update([
            'admin_reply' => $data[$field],
            'replied_at' => now(),
            'is_read' => true,
            'read_at' => $mensaje->read_at ?? now(),
        ]);

        return redirect()
            ->route('admin.contacto.inbox')
            ->with('status', 'Respuesta guardada. Puedes enviarla al correo del cliente con el enlace «Abrir correo».');
    }
}
