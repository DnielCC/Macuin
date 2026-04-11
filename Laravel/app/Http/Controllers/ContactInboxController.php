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
}
