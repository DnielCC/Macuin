<?php

namespace App\Services;

use App\Models\Macuin\Usuario;
use RuntimeException;

class PortalUsuarioResolver
{
    public function internalUserId(): int
    {
        $email = strtolower(trim((string) config('macuin.portal_usuario_email')));
        $u = Usuario::query()->whereRaw('LOWER(email) = ?', [$email])->first();
        if (! $u) {
            throw new RuntimeException(
                "No hay usuario interno (tabla usuarios) con el correo «{$email}». ".
                'Configura MACUIN_PORTAL_USUARIO_EMAIL en .env (por ejemplo ventas@macuin.com tras el seed).'
            );
        }

        return (int) $u->id;
    }
}
