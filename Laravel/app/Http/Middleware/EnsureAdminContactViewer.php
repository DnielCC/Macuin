<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureAdminContactViewer
{
    public function handle(Request $request, Closure $next): Response
    {
        $user = $request->user();
        if (! $user) {
            return redirect()->route('login')->with('error', 'Debes iniciar sesión para ver la bandeja.');
        }
        $allowed = config('macuin.admin_contact_emails', []);
        $email = strtolower(trim((string) $user->email));
        if ($allowed === []) {
            abort(503, 'La bandeja de contacto no está configurada. Define MACUIN_ADMIN_CONTACT_EMAILS en .env.');
        }
        if (! in_array($email, $allowed, true)) {
            abort(403, 'No tienes permiso para ver los mensajes de contacto.');
        }

        return $next($request);
    }
}
