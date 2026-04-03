@extends('layouts.app')

@section('title', 'Crear Nueva Cuenta')

@section('content')
<section class="min-h-[80vh] flex flex-col lg:flex-row">
    <div class="flex-1 flex items-center justify-center bg-white p-8 lg:p-12">
        <div class="w-full max-w-md bg-white rounded-xl shadow-lg border border-gray-100 p-8">
            <div class="flex items-center gap-2 mb-6">
                <span class="bg-black text-[var(--color-macuin-yellow)] font-bold text-lg px-2 py-0.5 rounded">M</span>
                <span class="font-bold text-gray-900">MACUIN</span>
            </div>
            <h1 class="text-2xl font-semibold text-gray-900 mb-6">Crear Nueva Cuenta</h1>
            @if ($errors->any())
                <div class="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                    <ul class="space-y-1">
                        @foreach ($errors->all() as $error)
                            <li>{{ $error }}</li>
                        @endforeach
                    </ul>
                </div>
            @endif

            <form action="{{ route('registro.store') }}" method="post" class="space-y-4">
                @csrf
                <div>
                    <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Nombre Completo</label>
                    <input type="text" id="name" name="name" placeholder="Juan Pérez García" required
                        value="{{ old('name') }}"
                        minlength="3"
                        maxlength="120"
                        autocomplete="name"
                        pattern="[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+"
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                    @error('name')
                        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Correo Electrónico</label>
                    <input type="email" id="email" name="email" placeholder="usuario@ejemplo.com" required
                        value="{{ old('email') }}"
                        maxlength="255"
                        autocomplete="email"
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                    @error('email')
                        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>
                <div>
                    <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
                    <input type="tel" id="phone" name="phone" placeholder="+52 55 1234 5678"
                        value="{{ old('phone') }}"
                        inputmode="tel"
                        maxlength="20"
                        autocomplete="tel"
                        pattern="^\+?[0-9\s\-]{10,20}$"
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                    @error('phone')
                        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>
                <div>
                    <label for="company" class="block text-sm font-medium text-gray-700 mb-1">Empresa (Opcional)</label>
                    <input type="text" id="company" name="company" placeholder="Mi Empresa S.A."
                        value="{{ old('company') }}"
                        minlength="2"
                        maxlength="150"
                        autocomplete="organization"
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                    @error('company')
                        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>
                <div>
                    <label for="address" class="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
                    <input type="text" id="address" name="address" placeholder="Calle Principal #123, Ciudad"
                        value="{{ old('address') }}"
                        minlength="5"
                        maxlength="255"
                        autocomplete="street-address"
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                    @error('address')
                        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
                    <input type="password" id="password" name="password" required placeholder="********"
                        minlength="8"
                        maxlength="72"
                        autocomplete="new-password"
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                    <p class="mt-1 text-xs text-gray-500">Debe incluir letras, números y un símbolo.</p>
                    @error('password')
                        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>
                <div>
                    <label for="password_confirmation" class="block text-sm font-medium text-gray-700 mb-1">Confirmar Contraseña</label>
                    <input type="password" id="password_confirmation" name="password_confirmation" required placeholder="********"
                        minlength="8"
                        maxlength="72"
                        autocomplete="new-password"
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                    @error('password_confirmation')
                        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>
                <button type="submit" class="w-full bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-semibold py-3 rounded-lg uppercase text-sm tracking-wide transition">
                    Crear cuenta
                </button>
            </form>
            <p class="mt-6 text-center text-gray-600 text-sm">
                ¿Ya tienes una cuenta? <a href="/ingresar" class="text-amber-600 font-medium hover:underline">Inicia sesión aquí</a>
            </p>
        </div>
    </div>
    <div class="hidden lg:block lg:w-1/2 bg-gray-800 relative min-h-[400px]">
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
        <div class="absolute bottom-0 left-0 right-0 p-8 text-white">
            <h2 class="text-2xl font-bold mb-2">Únete a MACUIN</h2>
            <p class="text-gray-300">Acceso exclusivo a componentes automotrices premium</p>
        </div>
    </div>
</section>
@endsection
