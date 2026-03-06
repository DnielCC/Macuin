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
                <a href="{{ route('catalogo') }}" class="bg-[var(--color-macuin-yellow)] text-black font-semibold px-6 py-3 rounded-lg hover:opacity-90 transition">Ver Catálogo</a>
                <a href="{{ route('contacto') }}" class="border border-gray-500 text-white font-semibold px-6 py-3 rounded-lg hover:bg-white/10 transition">Contactar</a>
            </div>
        </div>
        <div class="flex-1 flex justify-center lg:justify-end">
            <div class="w-64 h-48 lg:w-80 lg:h-56 bg-gray-700 rounded-lg flex items-center justify-center text-gray-500">
                [Imagen motor/autopartes]
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

{{-- Categorías --}}
<section class="py-16 bg-gray-50">
    <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">Explora Nuestras Categorías</h2>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <a href="{{ route('catalogo', ['categoria' => 'frenos']) }}" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition text-center">
                <div class="w-14 h-14 rounded-full bg-red-100 flex items-center justify-center mx-auto mb-3">
                    <span class="text-2xl">🛞</span>
                </div>
                <h3 class="font-semibold text-gray-900">Frenos</h3>
                <p class="text-sm text-gray-500 mt-1">300+ productos</p>
            </a>
            <a href="{{ route('catalogo', ['categoria' => 'suspension']) }}" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition text-center">
                <div class="w-14 h-14 rounded-full bg-gray-200 flex items-center justify-center mx-auto mb-3">
                    <span class="text-2xl">🔩</span>
                </div>
                <h3 class="font-semibold text-gray-900">Suspensión</h3>
                <p class="text-sm text-gray-500 mt-1">200+ productos</p>
            </a>
            <a href="{{ route('catalogo', ['categoria' => 'motor']) }}" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition text-center">
                <div class="w-14 h-14 rounded-full bg-amber-100 flex items-center justify-center mx-auto mb-3">
                    <span class="text-2xl">⚙️</span>
                </div>
                <h3 class="font-semibold text-gray-900">Motor</h3>
                <p class="text-sm text-gray-500 mt-1">250+ productos</p>
            </a>
            <a href="{{ route('catalogo', ['categoria' => 'transmision']) }}" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition text-center">
                <div class="w-14 h-14 rounded-full bg-amber-100 flex items-center justify-center mx-auto mb-3">
                    <span class="text-2xl">⚡</span>
                </div>
                <h3 class="font-semibold text-gray-900">Transmisión</h3>
                <p class="text-sm text-gray-500 mt-1">150+ productos</p>
            </a>
        </div>
    </div>
</section>

{{-- CTA --}}
<section class="py-16 bg-[var(--color-macuin-yellow)]">
    <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">¿Listo para Mejorar tu Vehículo?</h2>
        <p class="text-gray-800 mb-6 max-w-xl mx-auto">Regístrate hoy y obtén acceso a ofertas exclusivas y venta al por mayor.</p>
        <a href="{{ route('registro') }}" class="inline-block bg-gray-900 text-white font-semibold px-8 py-3 rounded-lg hover:bg-gray-800 transition">Crear Cuenta Ahora</a>
    </div>
</section>
@endsection
