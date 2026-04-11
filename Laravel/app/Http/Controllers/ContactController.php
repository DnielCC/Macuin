<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreContactMessageRequest;
use App\Models\ContactMessage;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class ContactController extends Controller
{
    public function create(): View
    {
        $mensajesContacto = collect();
        if (Auth::check()) {
            $user = Auth::user();
            $emailNorm = strtolower(trim((string) $user->email));
            $mensajesContacto = ContactMessage::query()
                ->where(function ($q) use ($user, $emailNorm) {
                    $q->whereRaw('LOWER(TRIM(email)) = ?', [$emailNorm])
                        ->orWhere('user_id', $user->id);
                })
                ->orderByDesc('id')
                ->limit(50)
                ->get();
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

        ContactMessage::query()->create([
            'user_id' => $request->user()?->id,
            'name' => $v['name'],
            'email' => strtolower(trim($v['email'])),
            'phone' => $phone,
            'subject' => $v['subject'],
            'message' => $v['message'],
            'is_read' => false,
        ]);

        return redirect()
            ->route('contacto')
            ->with('status', 'Mensaje enviado. Nuestro equipo lo verá en la bandeja de contacto. Te responderemos pronto.');
    }
}
