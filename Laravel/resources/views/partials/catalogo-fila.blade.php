@php
    $stock = (int) ($p->inventario?->stock_actual ?? 0);
    $agotado = $stock < 1;
    $img = $p->imagen_url;
    if ($img && !\Illuminate\Support\Str::startsWith($img, ['http://', 'https://'])) {
        $img = asset(ltrim($img, '/'));
    }
@endphp
<article class="bg-white rounded-xl border border-gray-100 shadow-sm p-4 flex flex-col sm:flex-row gap-4 sm:items-center">
    <div class="shrink-0 w-full sm:w-28 h-40 sm:h-28 rounded-lg bg-gray-100 relative overflow-hidden flex items-center justify-center">
        @if($agotado)
            <span class="absolute inset-0 z-10 flex items-center justify-center bg-gray-900/75 text-white text-xs font-medium">Agotado</span>
        @endif
        @if($img)
            <img src="{{ $img }}" alt="" class="w-full h-full object-cover" loading="lazy">
        @else
            <span class="text-gray-400 text-xs">Sin imagen</span>
        @endif
    </div>
    <div class="flex-1 min-w-0">
        <div class="flex flex-wrap gap-2 text-xs">
            <span class="text-amber-800/90 font-medium">{{ $p->categoria?->nombre ?? '—' }}</span>
            <span class="text-gray-400">·</span>
            <span class="text-gray-500">{{ $p->marca?->nombre ?? '—' }}</span>
        </div>
        <h3 class="font-semibold text-gray-900 mt-1">{{ $p->nombre }}</h3>
        <p class="text-xs text-gray-400 mt-1">SKU <code>{{ $p->sku_codigo }}</code> · Stock: {{ $stock }}</p>
    </div>
    <div class="flex flex-col sm:items-end gap-3 shrink-0 w-full sm:w-auto">
        <p class="text-lg font-bold text-gray-900">${{ number_format((float) $p->precio_unitario, 2, '.', ',') }} <span class="text-xs font-normal text-gray-500">MXN</span></p>
        @auth
            @if($agotado)
                <button type="button" disabled class="w-full sm:w-44 py-2.5 rounded-lg bg-gray-200 text-gray-500 text-sm font-medium cursor-not-allowed">Sin stock</button>
            @else
                <form method="post" action="{{ route('carrito.agregar') }}" class="flex flex-col sm:flex-row gap-2 items-stretch sm:items-center w-full sm:w-auto">
                    @csrf
                    <input type="hidden" name="autoparte_id" value="{{ $p->id }}">
                    <input type="number" name="cantidad" value="1" min="1" max="999" class="w-full sm:w-20 rounded border-gray-300 text-sm">
                    <button type="submit" class="py-2.5 px-4 rounded-lg bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black text-sm font-medium transition whitespace-nowrap">Al carrito</button>
                </form>
            @endif
        @else
            <a href="{{ route('login') }}" class="text-center py-2.5 px-4 rounded-lg border border-amber-500 text-amber-700 text-sm font-medium">Inicia sesión</a>
        @endauth
    </div>
</article>
