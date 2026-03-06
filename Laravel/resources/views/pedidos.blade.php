@extends('layouts.app')

@section('title', 'Mis Pedidos')

@section('content')
<div class="container mx-auto px-4 py-12">
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Mis Pedidos</h1>
        <p class="text-gray-600 mt-1">Revisa el estado de tus pedidos y su historial</p>
    </div>

    <div class="max-w-md mx-auto bg-white rounded-xl border border-gray-100 shadow-sm p-8 text-center">
        <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8 4-8-4m0 0l8-4 8 4m0-6v12M4 7v12"/></svg>
        </div>
        <h2 class="text-xl font-semibold text-gray-900 mb-2">No tienes pedidos aún</h2>
        <p class="text-gray-500 mb-6">Explora nuestro catálogo y realiza tu primera compra</p>
        <a href="{{ route('catalogo') }}" class="inline-block bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-semibold px-8 py-3 rounded-lg transition">Ir al Catálogo</a>
    </div>
</div>
@endsection
