<?php

namespace App\Http\Controllers;

use App\Models\ContactMessage;
use Illuminate\View\View;

class AccountController extends Controller
{
    public function show(): View
    {
        $user = auth()->user();
        $emailNorm = strtolower(trim((string) $user->email));

        $mensajesContacto = ContactMessage::query()
            ->where(function ($q) use ($user, $emailNorm) {
                $q->whereRaw('LOWER(TRIM(email)) = ?', [$emailNorm])
                    ->orWhere('user_id', $user->id);
            })
            ->orderByDesc('id')
            ->limit(50)
            ->get();

        return view('auth.account', [
            'mensajesContacto' => $mensajesContacto,
        ]);
    }
}
