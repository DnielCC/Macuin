<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreContactMessageRequest;
use App\Models\ContactMessage;
use Illuminate\Http\RedirectResponse;
use Illuminate\View\View;

class ContactController extends Controller
{
    public function create(): View
    {
        return view('contacto');
    }

    public function store(StoreContactMessageRequest $request): RedirectResponse
    {
        $v = $request->validated();
        ContactMessage::query()->create([
            'user_id' => $request->user()?->id,
            'name' => $v['name'],
            'email' => strtolower(trim($v['email'])),
            'phone' => $v['phone'] ?? null,
            'subject' => $v['subject'],
            'message' => $v['message'],
            'is_read' => false,
        ]);

        return redirect()
            ->route('contacto')
            ->with('status', 'Mensaje enviado. Nuestro equipo lo verá en la bandeja de contacto. Te responderemos pronto.');
    }
}
