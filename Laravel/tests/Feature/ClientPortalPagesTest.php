<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ClientPortalPagesTest extends TestCase
{
    use RefreshDatabase;

    public function test_guest_can_open_pedidos_carrito_contacto_and_pago(): void
    {
        foreach (['/pedidos', '/carrito', '/contacto', '/pago'] as $path) {
            $this->get($path)->assertOk();
        }
    }
}
