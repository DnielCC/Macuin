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
            <form action="#" method="post" class="space-y-4">
                @csrf
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Correo Electrónico</label>
                    <input type="email" id="email" name="email" placeholder="usuario@ejemplo.com" required
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
                    <input type="password" id="password" name="password" required
                        class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                </div>
                <div class="flex items-center justify-between text-sm">
                    <label class="flex items-center gap-2">
                        <input type="checkbox" name="remember" class="rounded border-gray-300 text-amber-600 focus:ring-amber-500">
                        <span class="text-gray-600">Recordarme</span>
                    </label>
                    <a href="#" class="text-amber-600 hover:underline">¿Olvidaste tu contraseña?</a>
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
