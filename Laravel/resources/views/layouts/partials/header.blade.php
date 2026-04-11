{{-- Rutas relativas al mismo host/puerto que la página actual. --}}
<header class="bg-[#1a1a1a] text-white shadow">
    <div class="container mx-auto px-4 py-3 flex items-center justify-between flex-wrap gap-4">
        <a href="{{ url('/inicio') }}" class="flex items-center gap-2">
            <span class="bg-[var(--color-macuin-yellow)] text-black font-bold px-2 py-0.5 rounded text-sm">M</span>
            <span class="font-semibold text-lg">MACUIN</span>
            <span class="text-gray-400 text-xs hidden sm:inline">Automotrices y Más</span>
        </a>
        <nav class="flex items-center gap-4 sm:gap-6 flex-wrap">
            <a href="{{ route('inicio') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ request()->routeIs('inicio') ? 'text-[var(--color-macuin-yellow)]' : '' }}">Inicio</a>
            <a href="{{ route('catalogo') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ request()->routeIs('catalogo') ? 'text-[var(--color-macuin-yellow)]' : '' }}">Catálogo</a>
            @auth
                <a href="{{ route('pedidos') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ request()->routeIs('pedidos') ? 'text-[var(--color-macuin-yellow)]' : '' }}">Pedidos</a>
            @else
                <a href="{{ route('login') }}" class="hover:text-[var(--color-macuin-yellow)] transition text-gray-400 text-sm">Pedidos</a>
            @endauth
            <a href="{{ route('contacto') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ request()->routeIs('contacto') ? 'text-[var(--color-macuin-yellow)]' : '' }}">Contacto</a>
            @auth
                <a href="{{ route('pago') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ request()->routeIs('pago') ? 'text-[var(--color-macuin-yellow)]' : '' }}">Pago</a>
            @endauth
            @if (!empty($macuinShowContactInbox ?? false))
                <a href="{{ route('admin.contacto.inbox') }}" class="hover:text-[var(--color-macuin-yellow)] transition text-amber-200 text-sm">Bandeja</a>
            @endif
            <a href="{{ route('carrito') }}" id="macuin-nav-carrito" class="relative p-1.5 rounded hover:bg-white/10 {{ request()->routeIs('carrito') ? 'text-[var(--color-macuin-yellow)] ring-1 ring-[var(--color-macuin-yellow)]/40' : '' }}" title="Carrito">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
                @auth
                    @if(($macuinCarritoCount ?? 0) > 0)
                        <span id="macuin-cart-badge" class="absolute -top-0.5 -right-0.5 min-w-[1.1rem] h-[1.1rem] px-1 rounded-full bg-[var(--color-macuin-yellow)] text-black text-[10px] font-bold flex items-center justify-center">{{ $macuinCarritoCount > 99 ? '99+' : $macuinCarritoCount }}</span>
                    @else
                        <span id="macuin-cart-badge" class="hidden absolute -top-0.5 -right-0.5 min-w-[1.1rem] h-[1.1rem] px-1 rounded-full bg-[var(--color-macuin-yellow)] text-black text-[10px] font-bold flex items-center justify-center">0</span>
                    @endif
                @endauth
            </a>
            @auth
                <a href="{{ route('cuenta') }}" class="hover:text-[var(--color-macuin-yellow)] transition {{ request()->routeIs('cuenta') ? 'text-[var(--color-macuin-yellow)]' : '' }}">Mi cuenta</a>
                <form action="{{ route('logout') }}" method="post">
                    @csrf
                    <button type="submit" class="bg-[var(--color-macuin-yellow)] text-black font-medium px-4 py-2 rounded hover:opacity-90">
                        Salir
                    </button>
                </form>
            @else
                <a href="{{ route('login') }}" class="bg-[var(--color-macuin-yellow)] text-black font-medium px-4 py-2 rounded hover:opacity-90">Ingresar</a>
                <a href="{{ route('registro') }}" class="border border-[var(--color-macuin-yellow)] text-white px-4 py-2 rounded hover:bg-white/5">Unirme</a>
            @endauth
        </nav>
    </div>
</header>
