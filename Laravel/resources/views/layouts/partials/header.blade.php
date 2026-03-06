@php
    $current = request()->route() ? request()->route()->getName() : null;
@endphp
<header class="bg-[#1a1a1a] text-white shadow">
    <div class="container mx-auto px-4 py-3 flex items-center justify-between flex-wrap gap-4">
        <a href="{{ route('inicio') }}" class="flex items-center gap-2">
            <span class="bg-[var(--color-macuin-yellow)] text-black font-bold px-2 py-0.5 rounded text-sm">M</span>
            <span class="font-semibold text-lg">MACUIN</span>
            <span class="text-gray-400 text-xs hidden sm:inline">Automotrices y Más</span>
        </a>
        <nav class="flex items-center gap-6">
            <a href="{{ route('inicio') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ $current === 'inicio' ? 'text-[var(--color-macuin-yellow)]' : '' }}">Inicio</a>
            <a href="{{ route('catalogo') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ $current === 'catalogo' ? 'text-[var(--color-macuin-yellow)]' : '' }}">Catálogo</a>
            <a href="{{ route('pedidos') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ $current === 'pedidos' ? 'text-[var(--color-macuin-yellow)]' : '' }}">Pedidos</a>
            <a href="{{ route('contacto') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ $current === 'contacto' ? 'text-[var(--color-macuin-yellow)]' : '' }}">Contacto</a>
            <a href="{{ route('carrito') }}" class="p-1.5 rounded hover:bg-white/10" title="Carrito">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
            </a>
            <a href="{{ route('login') }}" class="bg-[var(--color-macuin-yellow)] text-black font-medium px-4 py-2 rounded hover:opacity-90">Ingresar</a>
            <a href="{{ route('registro') }}" class="border border-[var(--color-macuin-yellow)] text-white px-4 py-2 rounded hover:bg-white/5">Unirme</a>
        </nav>
    </div>
</header>
