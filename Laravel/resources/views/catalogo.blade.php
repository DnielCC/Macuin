@extends('layouts.app')

@section('title', 'Catálogo')

@section('content')
<div class="container mx-auto px-4 py-8">
    <div class="flex flex-col lg:flex-row gap-6 mb-6">
        <div class="flex-1 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-700">Categorías</h2>
            <div class="flex flex-wrap gap-2">
                <a href="{{ route('catalogo') }}" class="px-4 py-2 rounded-lg {{ !request('categoria') ? 'bg-[var(--color-macuin-yellow)] text-black font-medium' : 'bg-gray-200 text-gray-700 hover:bg-gray-300' }}">Todos</a>
                <a href="{{ route('catalogo', ['categoria' => 'filtros']) }}" class="px-4 py-2 rounded-lg {{ request('categoria') === 'filtros' ? 'bg-[var(--color-macuin-yellow)] text-black font-medium' : 'bg-gray-200 text-gray-700 hover:bg-gray-300' }}">Filtros</a>
                <a href="{{ route('catalogo', ['categoria' => 'sistema-electrico']) }}" class="px-4 py-2 rounded-lg {{ request('categoria') === 'sistema-electrico' ? 'bg-[var(--color-macuin-yellow)] text-black font-medium' : 'bg-gray-200 text-gray-700 hover:bg-gray-300' }}">Sistema Eléctrico</a>
                <a href="{{ route('catalogo', ['categoria' => 'frenos']) }}" class="px-4 py-2 rounded-lg {{ request('categoria') === 'frenos' ? 'bg-[var(--color-macuin-yellow)] text-black font-medium' : 'bg-gray-200 text-gray-700 hover:bg-gray-300' }}">Frenos</a>
                <a href="{{ route('catalogo', ['categoria' => 'suspension']) }}" class="px-4 py-2 rounded-lg {{ request('categoria') === 'suspension' ? 'bg-[var(--color-macuin-yellow)] text-black font-medium' : 'bg-gray-200 text-gray-700 hover:bg-gray-300' }}">Suspensión</a>
                <a href="{{ route('catalogo', ['categoria' => 'lubricantes']) }}" class="px-4 py-2 rounded-lg {{ request('categoria') === 'lubricantes' ? 'bg-[var(--color-macuin-yellow)] text-black font-medium' : 'bg-gray-200 text-gray-700 hover:bg-gray-300' }}">Lubricantes</a>
                <a href="{{ route('catalogo', ['categoria' => 'motor']) }}" class="px-4 py-2 rounded-lg {{ request('categoria') === 'motor' ? 'bg-[var(--color-macuin-yellow)] text-black font-medium' : 'bg-gray-200 text-gray-700 hover:bg-gray-300' }}">Motor</a>
                <a href="{{ route('catalogo', ['categoria' => 'enfriamiento']) }}" class="px-4 py-2 rounded-lg {{ request('categoria') === 'enfriamiento' ? 'bg-[var(--color-macuin-yellow)] text-black font-medium' : 'bg-gray-200 text-gray-700 hover:bg-gray-300' }}">Sistema de Enfriamiento</a>
            </div>
        </div>
        <div class="w-full lg:w-80">
            <div class="relative">
                <input type="search" placeholder="Buscar productos..." class="w-full rounded-lg border border-gray-300 pl-10 pr-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
            </div>
        </div>
    </div>

    @php
        $productos = [
            ['nombre' => 'Filtro de Aceite Premium', 'categoria' => 'Filtros', 'precio' => 12500, 'descuento' => null, 'agotado' => false],
            ['nombre' => 'Bujia de Iridio', 'categoria' => 'Sistema Eléctrico', 'precio' => 8900, 'precio_antes' => 10474, 'descuento' => 15, 'agotado' => false],
            ['nombre' => 'Pastillas de Freno', 'categoria' => 'Frenos', 'precio' => 45000, 'descuento' => null, 'agotado' => false],
            ['nombre' => 'Amortiguador Delantero', 'categoria' => 'Suspensión', 'precio' => 125000, 'precio_antes' => 130099, 'descuento' => 10, 'agotado' => false],
            ['nombre' => 'Bateria 12V 75Ah', 'categoria' => 'Sistema Eléctrico', 'precio' => 95000, 'descuento' => null, 'agotado' => true],
            ['nombre' => 'Aceite de Motor 5W-30', 'categoria' => 'Lubricantes', 'precio' => 18500, 'descuento' => null, 'agotado' => false],
            ['nombre' => 'Correa de Distribución', 'categoria' => 'Motor', 'precio' => 32000, 'descuento' => null, 'agotado' => false],
            ['nombre' => 'Radiador de Aluminio', 'categoria' => 'Sistema de Enfriamiento', 'precio' => 78000, 'descuento' => null, 'agotado' => false],
        ];
    @endphp

    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        @foreach($productos as $p)
            <article class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md transition">
                <div class="aspect-square bg-gray-100 relative flex items-center justify-center text-gray-400">
                    @if($p['agotado'])
                        <span class="absolute inset-0 flex items-center justify-center bg-gray-800/80 text-white font-medium">Agotado</span>
                    @elseif(isset($p['descuento']))
                        <span class="absolute top-2 right-2 bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded">-{{ $p['descuento'] }}%</span>
                    @endif
                    [IMG]
                </div>
                <div class="p-4">
                    <span class="text-xs text-gray-500">{{ $p['categoria'] }}</span>
                    <h3 class="font-medium text-gray-900 mt-0.5">{{ $p['nombre'] }}</h3>
                    <div class="flex items-baseline gap-2 mt-2">
                        <span class="font-semibold text-gray-900">${{ number_format($p['precio'], 0, ',', '.') }}</span>
                        @if(isset($p['precio_antes']))
                            <span class="text-sm text-gray-400 line-through">${{ number_format($p['precio_antes'], 0, ',', '.') }}</span>
                        @endif
                    </div>
                    @if($p['agotado'])
                        <button disabled class="w-full mt-3 py-2.5 rounded-lg bg-gray-200 text-gray-500 font-medium cursor-not-allowed">Agotado</button>
                    @else
                        <a href="{{ route('carrito') }}" class="block w-full mt-3 py-2.5 rounded-lg bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-medium text-center transition">Agregar al carrito</a>
                    @endif
                </div>
            </article>
        @endforeach
    </div>
</div>
@endsection
