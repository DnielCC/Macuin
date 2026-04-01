<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class AuthenticationTest extends TestCase
{
    use RefreshDatabase;

    public function test_a_client_can_register_with_extended_profile_data(): void
    {
        $response = $this->withSession(['_token' => 'test-token'])->post('/registro', [
            '_token' => 'test-token',
            'name' => 'Juan Perez',
            'email' => 'juan@example.com',
            'phone' => '+52 55 1234 5678',
            'company' => 'Macuin Talleres',
            'address' => 'Av. Principal 123',
            'password' => 'Password123!',
            'password_confirmation' => 'Password123!',
        ]);

        $response->assertRedirect('/mi-cuenta');
        $this->assertAuthenticated();
        $this->assertDatabaseHas('users', [
            'email' => 'juan@example.com',
            'phone' => '+52 55 1234 5678',
            'company' => 'Macuin Talleres',
            'address' => 'Av. Principal 123',
        ]);
    }

    public function test_a_client_can_log_in_with_valid_credentials(): void
    {
        $user = User::factory()->create([
            'email' => 'cliente@example.com',
            'password' => 'Password123!',
        ]);

        $response = $this->withSession(['_token' => 'test-token'])->post('/ingresar', [
            '_token' => 'test-token',
            'email' => $user->email,
            'password' => 'Password123!',
        ]);

        $response->assertRedirect('/mi-cuenta');
        $this->assertAuthenticatedAs($user);
    }

    public function test_login_with_unknown_credentials_returns_to_the_same_interface_with_an_error(): void
    {
        $response = $this
            ->from('/ingresar')
            ->withSession(['_token' => 'test-token'])
            ->post('/ingresar', [
                '_token' => 'test-token',
                'email' => 'noexiste@example.com',
                'password' => 'Password123!',
            ]);

        $response->assertRedirect('/ingresar');
        $response->assertSessionHasErrors('email');
        $this->assertGuest();
    }

    public function test_register_validation_returns_to_the_same_interface_with_errors(): void
    {
        $response = $this
            ->from('/registro')
            ->withSession(['_token' => 'test-token'])
            ->post('/registro', [
                '_token' => 'test-token',
                'name' => '12',
                'email' => 'correo-invalido',
                'phone' => 'abc',
                'company' => 'A',
                'address' => '123',
                'password' => '12345678',
                'password_confirmation' => '87654321',
            ]);

        $response->assertRedirect('/registro');
        $response->assertSessionHasErrors([
            'name',
            'email',
            'phone',
            'company',
            'address',
            'password',
        ]);
    }

    public function test_guest_users_cannot_access_the_account_page(): void
    {
        $response = $this->get('/mi-cuenta');

        $response->assertRedirect('/ingresar');
    }
}
