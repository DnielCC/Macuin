@php
    $stock = (int) ($p->inventario?->stock_actual ?? 0);
    $agotado = $stock < 1;
    $img = $p->imagen_url;
    if ($img && !\Illuminate\Support\Str::startsWith($img, ['http://', 'https://'])) {
        $img = asset(ltrim($img, '/'));
    }
@endphp
<article class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md transition flex flex-col h-full">
    <div class="aspect-square bg-gray-100 relative flex items-center justify-center text-gray-400 text-sm">
        @if($agotado)
            <span class="absolute inset-0 z-10 flex items-center justify-center bg-gray-900/75 text-white font-medium text-sm">Agotado</span>
        @endif
        @if($img)
            <img src="{{ $img }}" alt="{{ $p->nombre }}" class="w-full h-full object-cover" loading="lazy">
        @else
            <span class="text-gray-400 text-xs px-2 text-center">Sin imagen</span>
        @endif
    </div>
    <div class="p-4 flex flex-col flex-1">
        <span class="text-xs text-amber-800/80 font-medium">{{ $p->categoria?->nombre ?? '—' }}</span>
        <span class="text-[11px] text-gray-400">{{ $p->marca?->nombre ?? '—' }}</span>
        <h3 class="font-medium text-gray-900 mt-1 line-clamp-2">{{ $p->nombre }}</h3>
        <p class="text-xs text-gray-400 mt-1">SKU <code class="text-gray-500">{{ $p->sku_codigo }}</code></p>
        <p class="text-xs {{ $stock <= ($p->inventario?->stock_minimo ?? 0) && !$agotado ? 'text-amber-600' : 'text-gray-500' }} mt-1">Existencias: {{ $stock }}</p>
        <div class="mt-auto pt-3">
            <p class="font-semibold text-gray-900">${{ number_format((float) $p->precio_unitario, 2, '.', ',') }} <span class="text-xs font-normal text-gray-500">MXN</span></p>
            @auth
                @if($agotado)
                    <button type="button" disabled class="w-full mt-3 py-2.5 rounded-lg bg-gray-200 text-gray-500 text-sm font-medium cursor-not-allowed">Sin stock</button>
                @else
                    <form method="post" action="{{ route('carrito.agregar') }}" class="mt-3">
                        @csrf
                        <input type="hidden" name="autoparte_id" value="{{ $p->id }}">
                        <div class="flex gap-2 items-center">
                            <input type="number" name="cantidad" value="1" min="1" max="999" class="w-16 rounded border-gray-300 text-sm">
                            <button type="submit" class="flex-1 py-2.5 rounded-lg bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black text-sm font-medium transition">Al carrito</button>
                        </div>
                    </form>
                @endif
            @else
                <a href="{{ route('login') }}" class="block w-full mt-3 py-2.5 rounded-lg border border-amber-500 text-amber-700 font-medium text-center text-sm">Inicia sesión para comprar</a>
            @endauth
        </div>
    </div>
</article>
