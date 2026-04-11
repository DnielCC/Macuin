@extends('layouts.app')

@section('title', 'Inicio')

@section('content')
{{-- Hero --}}
<section class="bg-gradient-to-br from-gray-800 to-gray-900 text-white py-16 lg:py-24">
    <div class="container mx-auto px-4 flex flex-col lg:flex-row items-center gap-12">
        <div class="flex-1">
            <h1 class="text-4xl lg:text-5xl font-bold mb-4">Componentes Automotrices de Alta Calidad</h1>
            <p class="text-gray-300 text-lg mb-8">Encuentra las mejores piezas para tu vehículo. Calidad, precios competitivos y entrega rápida.</p>
            <div class="flex flex-wrap gap-4">
                <a href="{{ route('catalogo') }}" class="bg-[var(--color-macuin-yellow)] text-black font-semibold px-6 py-3 rounded-lg hover:opacity-90 transition">Ver catálogo</a>
                <a href="{{ route('contacto') }}" class="border border-gray-500 text-white font-semibold px-6 py-3 rounded-lg hover:bg-white/10 transition">Contactar</a>
            </div>
        </div>
        <div class="flex-1 flex justify-center lg:justify-end">
            <div class="w-64 h-48 lg:w-80 lg:h-56 rounded-lg bg-gradient-to-br from-gray-700 to-gray-900 ring-1 ring-white/10 flex items-center justify-center text-gray-400 text-sm px-4 text-center">
                Catálogo en línea con existencias reales
            </div>
        </div>
    </div>
</section>

{{-- ¿Por qué MACUIN? --}}
<section id="nosotros" class="py-16 bg-white">
    <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">¿Por Qué Elegir MACUIN?</h2>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
            <div class="text-center">
                <div class="w-16 h-16 rounded-full bg-amber-100 flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Calidad Garantizada</h3>
                <p class="text-gray-600 text-sm">Todos nuestros componentes tienen garantía, para su tranquilidad y satisfacción en la compra.</p>
            </div>
            <div class="text-center">
                <div class="w-16 h-16 rounded-full bg-amber-100 flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Envío Rápido</h3>
                <p class="text-gray-600 text-sm">Entrega en un corto tiempo, para que regreses a la carretera lo antes posible.</p>
            </div>
            <div class="text-center">
                <div class="w-16 h-16 rounded-full bg-amber-100 flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Repuestos</h3>
                <p class="text-gray-600 text-sm">Amplia variedad de repuestos automotrices para que encuentres lo que necesitas.</p>
            </div>
            <div class="text-center">
                <div class="w-16 h-16 rounded-full bg-amber-100 flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Soporte Técnico</h3>
                <p class="text-gray-600 text-sm">Equipo de expertos para ayudarte a elegir y diagnosticar tu vehículo.</p>
            </div>
        </div>
    </div>
</section>

{{-- Categorías (desde PostgreSQL) --}}
<section class="py-16 bg-gray-50">
    <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-4">Explora nuestras categorías</h2>
        <p class="text-center text-gray-600 text-sm mb-12 max-w-2xl mx-auto">Los enlaces llevan al catálogo filtrado por <code class="text-xs">categoria_id</code> según los datos actuales de la base.</p>
        @if($categoriasDestacadas->isEmpty())
            <p class="text-center text-gray-500 text-sm">Cuando existan categorías en la base de datos, aparecerán aquí automáticamente.</p>
        @else
            <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
                @foreach($categoriasDestacadas as $cat)
                    <a href="{{ route('catalogo', ['categoria_id' => $cat->id]) }}" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-amber-200/60 transition text-center block">
                        <div class="w-14 h-14 rounded-full bg-amber-100 flex items-center justify-center mx-auto mb-3">
                            <svg class="w-7 h-7 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                        </div>
                        <h3 class="font-semibold text-gray-900">{{ $cat->nombre }}</h3>
                        <p class="text-sm text-gray-500 mt-1">{{ $cat->autopartes_count }} {{ $cat->autopartes_count === 1 ? 'producto' : 'productos' }}</p>
                    </a>
                @endforeach
            </div>
            <p class="text-center mt-8">
                <a href="{{ route('catalogo') }}" class="text-amber-700 font-medium hover:underline text-sm">Ver catálogo completo</a>
            </p>
        @endif
    </div>
</section>

{{-- CTA --}}
<section class="py-16 bg-[var(--color-macuin-yellow)]">
    <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">¿Listo para Mejorar tu Vehículo?</h2>
        <p class="text-gray-800 mb-6 max-w-xl mx-auto">Regístrate hoy y obtén acceso a ofertas exclusivas y venta al por mayor.</p>
        <a href="{{ route('registro') }}" class="inline-block bg-gray-900 text-white font-semibold px-8 py-3 rounded-lg hover:bg-gray-800 transition">Crear cuenta ahora</a>
    </div>
</section>
@endsection
