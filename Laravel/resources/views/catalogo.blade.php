@extends('layouts.app')

@section('title', 'Catálogo')

@section('content')
@php
    $querySinPagina = request()->except('page');
@endphp
<div class="container mx-auto px-4 py-8">
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-6">
        <div>
            <h1 class="text-2xl font-bold text-gray-900">Catálogo</h1>
            <p class="text-sm text-gray-500 mt-1">Productos desde PostgreSQL: tablas <code class="text-xs">autopartes</code>, <code class="text-xs">inventarios</code>, <code class="text-xs">categorias</code>, <code class="text-xs">marcas</code>.</p>
        </div>
        <div class="flex items-center gap-2 shrink-0">
            <span class="text-xs text-gray-500 uppercase tracking-wide hidden sm:inline">Vista</span>
            <a href="{{ route('catalogo', array_merge($querySinPagina, ['vista' => 'mosaico'])) }}"
               class="p-2.5 rounded-lg border transition {{ $vista === 'mosaico' ? 'bg-[var(--color-macuin-yellow)] border-amber-500 text-black' : 'bg-white border-gray-200 text-gray-600 hover:border-gray-300' }}"
               title="Mosaico">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3h7v7H3V3zm11 0h7v7h-7V3zM3 14h7v7H3v-7zm11 0h7v7h-7v-7z"/></svg>
            </a>
            <a href="{{ route('catalogo', array_merge($querySinPagina, ['vista' => 'lista'])) }}"
               class="p-2.5 rounded-lg border transition {{ $vista === 'lista' ? 'bg-[var(--color-macuin-yellow)] border-amber-500 text-black' : 'bg-white border-gray-200 text-gray-600 hover:border-gray-300' }}"
               title="Lista">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16v2H4V6zm0 5h16v2H4v-2zm0 5h16v2H4v-2z"/></svg>
            </a>
        </div>
    </div>

    {{-- Panel de filtros --}}
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-5 mb-8">
        <form method="get" action="{{ route('catalogo') }}" class="space-y-5">
            <input type="hidden" name="vista" value="{{ $vista }}">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-gray-100 pb-3">
                <h2 class="text-sm font-semibold text-gray-800 uppercase tracking-wide">Filtros</h2>
                <a href="{{ route('catalogo', ['vista' => $vista]) }}" class="text-sm text-amber-700 hover:underline font-medium">Limpiar filtros</a>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                    <label for="filtro-categoria" class="block text-xs font-medium text-gray-500 mb-1">Categoría</label>
                    <select id="filtro-categoria" name="categoria_id" class="w-full rounded-lg border-gray-300 text-sm shadow-sm focus:border-amber-500 focus:ring-amber-500">
                        <option value="">Todas</option>
                        @foreach($categorias as $cat)
                            <option value="{{ $cat->id }}" @selected((int) ($categoriaId ?? 0) === (int) $cat->id)>{{ $cat->nombre }}</option>
                        @endforeach
                    </select>
                </div>
                <div>
                    <label for="filtro-marca" class="block text-xs font-medium text-gray-500 mb-1">Marca</label>
                    <select id="filtro-marca" name="marca_id" class="w-full rounded-lg border-gray-300 text-sm shadow-sm focus:border-amber-500 focus:ring-amber-500">
                        <option value="">Todas</option>
                        @foreach($marcas as $m)
                            <option value="{{ $m->id }}" @selected((int) ($marcaId ?? 0) === (int) $m->id)>{{ $m->nombre }}</option>
                        @endforeach
                    </select>
                </div>
                <div>
                    <label for="filtro-orden" class="block text-xs font-medium text-gray-500 mb-1">Ordenar por</label>
                    <select id="filtro-orden" name="orden" class="w-full rounded-lg border-gray-300 text-sm shadow-sm focus:border-amber-500 focus:ring-amber-500">
                        <option value="nombre_asc" @selected($orden === 'nombre_asc')>Nombre (A–Z)</option>
                        <option value="precio_asc" @selected($orden === 'precio_asc')>Precio: menor a mayor</option>
                        <option value="precio_desc" @selected($orden === 'precio_desc')>Precio: mayor a menor</option>
                        <option value="recientes" @selected($orden === 'recientes')>Más recientes</option>
                    </select>
                </div>
                <div>
                    <label for="filtro-stock" class="block text-xs font-medium text-gray-500 mb-1">Disponibilidad</label>
                    <select id="filtro-stock" name="stock" class="w-full rounded-lg border-gray-300 text-sm shadow-sm focus:border-amber-500 focus:ring-amber-500">
                        <option value="todos" @selected($stock === 'todos')>Todos los productos</option>
                        <option value="con" @selected($stock === 'con')>Solo con existencias</option>
                    </select>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-3 sm:items-end">
                <div class="flex-1">
                    <label for="filtro-q" class="block text-xs font-medium text-gray-500 mb-1">Buscar por nombre o SKU</label>
                    <div class="relative">
                        <input id="filtro-q" type="search" name="q" value="{{ $qRaw }}" maxlength="120" placeholder="Ej. filtro, SKU-001…"
                               class="w-full rounded-lg border-gray-300 pl-10 pr-4 py-2.5 text-sm shadow-sm focus:border-amber-500 focus:ring-amber-500">
                        <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                    </div>
                </div>
                <button type="submit" class="w-full sm:w-auto shrink-0 px-8 py-2.5 rounded-lg bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-semibold text-sm transition shadow-sm">
                    Aplicar filtros
                </button>
            </div>
        </form>
    </div>

    @if($productos->isEmpty())
        <div class="rounded-xl border border-dashed border-gray-300 bg-white p-12 text-center text-gray-600">
            <p class="font-medium text-gray-800 mb-1">No hay productos que coincidan</p>
            <p class="text-sm">Prueba otros filtros o revisa que existan registros en <code class="text-xs">autopartes</code> en la base de datos.</p>
        </div>
    @else
        @if($vista === 'lista')
            <div class="space-y-4">
                @foreach($productos as $p)
                    @include('partials.catalogo-fila', ['p' => $p])
                @endforeach
            </div>
        @else
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                @foreach($productos as $p)
                    @include('partials.catalogo-tarjeta', ['p' => $p])
                @endforeach
            </div>
        @endif

        @if(method_exists($productos, 'hasPages') && $productos->hasPages())
            <div class="mt-10 flex justify-center">
                {{ $productos->links() }}
            </div>
        @endif
    @endif
</div>
@endsection
