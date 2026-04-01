<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Str;
use Illuminate\View\View;

class AuthenticatedSessionController extends Controller
{
    public function create(): View
    {
        return view('auth.login');
    }

    public function store(Request $request): RedirectResponse
    {
        $credentials = $request->validate(
            [
                'email' => ['required', 'string', 'email:rfc', 'max:255'],
                'password' => ['required', 'string', 'min:8', 'max:72'],
            ],
            [
                'email.required' => 'El correo electrónico es obligatorio.',
                'email.email' => 'Ingresa un correo electrónico válido.',
                'email.max' => 'El correo electrónico no puede exceder 255 caracteres.',
                'password.required' => 'La contraseña es obligatoria.',
                'password.min' => 'La contraseña debe tener al menos 8 caracteres.',
                'password.max' => 'La contraseña no puede exceder 72 caracteres.',
            ],
            [
                'email' => 'correo electrónico',
                'password' => 'contraseña',
            ]
        );

        $credentials['email'] = Str::lower(trim($credentials['email']));

        $remember = $request->boolean('remember');

        if (! Auth::attempt($credentials, $remember)) {
            return back()
                ->withErrors([
                    'email' => 'No encontramos una cuenta con esas credenciales. Verifica tu correo y contraseña o regístrate primero.',
                ])
                ->onlyInput('email', 'remember');
        }

        $request->session()->regenerate();

        return redirect()->intended(route('cuenta'))->with('status', 'Sesion iniciada correctamente.');
    }

    public function destroy(Request $request): RedirectResponse
    {
        Auth::guard('web')->logout();

        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect()->route('login')->with('status', 'Sesion cerrada correctamente.');
    }
}
