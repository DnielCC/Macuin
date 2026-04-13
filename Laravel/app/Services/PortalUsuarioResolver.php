<?php

namespace App\Services;

class PortalUsuarioResolver
{
    public function internalUserEmail(): string
    {
        $email = strtolower(trim((string) config('macuin.portal_usuario_email', 'alidaniel@macuin.com')));
        return $email;
    }
}
