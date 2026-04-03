@extends('layouts.app')

@section('title', 'Contáctanos')

@section('content')
<div class="container mx-auto px-4 py-12">
    <div class="flex flex-col lg:flex-row justify-between gap-4 mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Contáctanos</h1>
        <a href="/catalogo" class="text-amber-600 hover:underline font-medium">Volver al Catálogo</a>
    </div>
    <p class="text-gray-600 mb-10">Estamos aquí para ayudarte con tus necesidades automotrices.</p>

    <div class="grid lg:grid-cols-3 gap-8">
        <div class="lg:col-span-1 space-y-4">
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <div class="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center mb-3">
                    <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Teléfono</h3>
                <p class="text-gray-600 text-sm">+52 55 1234 5678</p>
                <p class="text-gray-600 text-sm">+52 55 8765 4321</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <div class="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center mb-3">
                    <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Email</h3>
                <p class="text-gray-600 text-sm">ventas@macuin.com</p>
                <p class="text-gray-600 text-sm">soporte@macuin.com</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <div class="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center mb-3">
                    <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Dirección</h3>
                <p class="text-gray-600 text-sm">Av. Industrial #1234</p>
                <p class="text-gray-600 text-sm">Col. Zona Industrial</p>
                <p class="text-gray-600 text-sm">Ciudad de México, 01234</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <div class="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center mb-3">
                    <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Horario de Atención</h3>
                <p class="text-gray-600 text-sm">Lunes - Viernes: 8:00 - 18:00</p>
                <p class="text-gray-600 text-sm">Sábado: 9:00 - 14:00</p>
                <p class="text-gray-600 text-sm">Domingo: Cerrado</p>
            </div>
        </div>
        <div class="lg:col-span-2">
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-8">
                <h2 class="text-xl font-semibold text-gray-900 mb-1">Envíanos un Mensaje</h2>
                <p class="text-gray-500 text-sm mb-6">Responderemos a la brevedad posible</p>
                <p class="text-sm text-gray-600 border border-dashed border-gray-200 rounded-lg px-4 py-8 text-center bg-gray-50">
                    Vista estática: aquí irá el formulario de contacto cuando se active la funcionalidad. Usa los datos de la columna izquierda para comunicarte por ahora.
                </p>
            </div>
        </div>
    </div>
</div>
@endsection
