<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ClientPortalPagesTest extends TestCase
{
    use RefreshDatabase;

    public function test_guest_can_open_catalogo_and_contacto(): void
    {
        $this->get('/catalogo')->assertOk();
        $this->get('/contacto')->assertOk();
    }

    public function test_guest_is_redirected_from_portal_protegido(): void
    {
        foreach (['/pedidos', '/carrito', '/pago'] as $path) {
            $this->get($path)->assertRedirect(route('login'));
        }
    }
}
