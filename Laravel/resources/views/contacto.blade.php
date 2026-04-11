@extends('layouts.app')

@section('title', 'Contáctanos')

@section('content')
<div class="container mx-auto px-4 py-12">
    <div class="flex flex-col lg:flex-row justify-between gap-4 mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Contáctanos</h1>
        <a href="{{ route('catalogo') }}" class="text-amber-600 hover:underline font-medium">Volver al catálogo</a>
    </div>
    <p class="text-gray-600 mb-10">Tu mensaje queda guardado en la base de datos para que el equipo administrador lo revise en la bandeja del portal.</p>

    <div class="grid lg:grid-cols-3 gap-8">
        <div class="lg:col-span-1 space-y-4">
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <h3 class="font-semibold text-gray-900 mb-2">Correo</h3>
                <p class="text-gray-600 text-sm">ventas@macuin.com</p>
                <p class="text-gray-600 text-sm">soporte@macuin.com</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6 text-sm text-gray-600">
                <p>Los mensajes del formulario se listan en <strong class="text-gray-800">Bandeja</strong> (solo cuentas administrador configuradas en <code class="text-xs">MACUIN_ADMIN_CONTACT_EMAILS</code>).</p>
            </div>
        </div>
        <div class="lg:col-span-2">
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-8">
                <h2 class="text-xl font-semibold text-gray-900 mb-1">Envíanos un mensaje</h2>
                <p class="text-gray-500 text-sm mb-6">Responderemos lo antes posible.</p>

                <form method="post" action="{{ route('contacto.store') }}" class="space-y-4">
                    @csrf
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Nombre</label>
                        <input type="text" name="name" value="{{ old('name', auth()->user()?->name) }}" required maxlength="200" class="mt-1 w-full rounded-lg border-gray-300 @error('name') border-red-500 @enderror">
                        @error('name')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Correo</label>
                        <input type="email" name="email" value="{{ old('email', auth()->user()?->email) }}" required maxlength="255" class="mt-1 w-full rounded-lg border-gray-300 @error('email') border-red-500 @enderror">
                        @error('email')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Teléfono (opcional)</label>
                        <input type="text" name="phone" value="{{ old('phone', auth()->user()?->phone) }}" maxlength="40" class="mt-1 w-full rounded-lg border-gray-300">
                        @error('phone')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Asunto</label>
                        <input type="text" name="subject" value="{{ old('subject') }}" required maxlength="200" class="mt-1 w-full rounded-lg border-gray-300">
                        @error('subject')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Mensaje</label>
                        <textarea name="message" rows="6" required maxlength="5000" class="mt-1 w-full rounded-lg border-gray-300">{{ old('message') }}</textarea>
                        @error('message')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
                    </div>
                    <button type="submit" class="w-full sm:w-auto px-6 py-3 rounded-lg bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-semibold transition">Enviar mensaje</button>
                </form>
            </div>
        </div>
    </div>
</div>
@endsection
