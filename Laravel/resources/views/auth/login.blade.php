@extends('layouts.app')

@section('title', 'Acceso al Portal de Clientes')

@section('content')
<section class="min-h-[80vh] flex flex-col lg:flex-row">
    <div class="flex-1 flex items-center justify-center bg-white p-8 lg:p-12">
        <div class="w-full max-w-md bg-white rounded-xl shadow-lg border border-gray-100 p-8">
            <div class="flex items-center gap-2 mb-6">
                <span class="bg-black text-[var(--color-macuin-yellow)] font-bold text-lg px-2 py-0.5 rounded">M</span>
                <span class="font-bold text-gray-900">MACUIN</span>
            </div>
            <h1 class="text-2xl font-semibold text-gray-900 mb-6">Acceso al Portal de Clientes</h1>
            @if (session('status'))
                <div class="mb-4 rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
                    {{ session('status') }}
                </div>
            @endif

            @if ($errors->any())
                <div class="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                    {{ $errors->first() }}
                </div>
            @endif

            <form action="{{ route('login.store') }}" method="post" class="space-y-4">
                @csrf
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Correo Electrónico</label>
                    <input type="email" id="email" name="email" placeholder="usuario@ejemplo.com" required
                        value="{{ old('email') }}"
                        maxlength="255"
                        autocomplete="email"
                        class="w-full rounded-lg border {{ $errors->has('email') ? 'border-red-400' : 'border-gray-300' }} px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                    @error('email')
                        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
                    <input type="password" id="password" name="password" required
                        minlength="8"
                        maxlength="72"
                        autocomplete="current-password"
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                    @error('password')
                        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>
                <div class="flex items-center justify-between text-sm">
                    <label class="flex items-center gap-2">
                        <input type="checkbox" name="remember" class="rounded border-gray-300 text-amber-600 focus:ring-amber-500" {{ old('remember') ? 'checked' : '' }}>
                        <span class="text-gray-600">Recordarme</span>
                    </label>
                    <span class="text-gray-400 cursor-not-allowed" title="Funcionalidad disponible en una siguiente fase">¿Olvidaste tu contraseña?</span>
                </div>
                <button type="submit" class="w-full bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-semibold py-3 rounded-lg uppercase text-sm tracking-wide transition">
                    Iniciar sesión
                </button>
            </form>
            <p class="mt-6 text-center text-gray-600 text-sm">
                ¿No tienes una cuenta? <a href="{{ route('registro') }}" class="text-amber-600 font-medium hover:underline">Regístrate aquí</a>
            </p>
        </div>
    </div>
    <div class="hidden lg:block lg:w-1/2 bg-gray-800 relative min-h-[400px]">
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
        <div class="absolute bottom-0 left-0 right-0 p-8 text-white">
            <h2 class="text-2xl font-bold mb-2">Robustez y Eficiencia</h2>
            <p class="text-gray-300">Componentes automotrices de alta calidad para profesionales exigentes</p>
        </div>
    </div>
</section>
@endsection
