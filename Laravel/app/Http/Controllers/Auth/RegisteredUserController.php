<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Illuminate\Validation\Rules\Password;
use Illuminate\View\View;

class RegisteredUserController extends Controller
{
    public function create(): View
    {
        return view('auth.register');
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $request->validate(
            [
                'name' => ['required', 'string', 'min:3', 'max:120', 'regex:/^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/u'],
                'email' => ['required', 'string', 'email:rfc', 'max:255', 'unique:'.User::class],
                'phone' => ['nullable', 'string', 'max:20', 'regex:/^\+?[0-9\s\-]{10,20}$/'],
                'company' => ['nullable', 'string', 'min:2', 'max:150'],
                'address' => ['nullable', 'string', 'min:5', 'max:255'],
                'password' => ['required', 'confirmed', 'max:72', Password::min(8)->letters()->numbers()->symbols()],
            ],
            [
                'name.required' => 'El nombre completo es obligatorio.',
                'name.min' => 'El nombre completo debe tener al menos 3 caracteres.',
                'name.max' => 'El nombre completo no puede exceder 120 caracteres.',
                'name.regex' => 'El nombre completo solo puede contener letras y espacios.',
                'email.required' => 'El correo electrónico es obligatorio.',
                'email.email' => 'Ingresa un correo electrónico válido.',
                'email.max' => 'El correo electrónico no puede exceder 255 caracteres.',
                'email.unique' => 'Ya existe una cuenta registrada con este correo electrónico.',
                'phone.max' => 'El teléfono no puede exceder 20 caracteres.',
                'phone.regex' => 'Ingresa un teléfono válido con 10 a 20 caracteres numéricos.',
                'company.min' => 'La empresa debe tener al menos 2 caracteres.',
                'company.max' => 'La empresa no puede exceder 150 caracteres.',
                'address.min' => 'La dirección debe tener al menos 5 caracteres.',
                'address.max' => 'La dirección no puede exceder 255 caracteres.',
                'password.required' => 'La contraseña es obligatoria.',
                'password.confirmed' => 'La confirmación de la contraseña no coincide.',
                'password.min' => 'La contraseña debe tener al menos 8 caracteres.',
                'password.letters' => 'La contraseña debe incluir al menos una letra.',
                'password.numbers' => 'La contraseña debe incluir al menos un número.',
                'password.symbols' => 'La contraseña debe incluir al menos un símbolo.',
                'password.max' => 'La contraseña no puede exceder 72 caracteres.',
            ],
            [
                'name' => 'nombre completo',
                'email' => 'correo electrónico',
                'phone' => 'teléfono',
                'company' => 'empresa',
                'address' => 'dirección',
                'password' => 'contraseña',
            ]
        );

        $validated['email'] = Str::lower(trim($validated['email']));

        $user = User::create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'phone' => $validated['phone'] ?? null,
            'company' => $validated['company'] ?? null,
            'address' => $validated['address'] ?? null,
            'password' => Hash::make($validated['password']),
        ]);

        Auth::login($user);
        $request->session()->regenerate();

        return redirect()->route('cuenta')->with('status', 'Tu cuenta fue creada correctamente.');
    }
}
