@extends('layouts.app')

@section('title', 'Carrito de compras')

@section('content')
<div class="container mx-auto px-4 py-8">
    <div class="flex justify-end mb-6">
        <a href="{{ route('catalogo') }}" class="text-amber-600 hover:underline font-medium">Seguir comprando</a>
    </div>

    @if(!$carrito || $carrito->lineas->isEmpty())
        <div class="max-w-xl mx-auto rounded-xl border border-gray-200 bg-white p-10 text-center text-gray-600">
            <p class="font-semibold text-gray-900 mb-2">Tu carrito está vacío</p>
            <p class="text-sm mb-4">Agrega productos desde el catálogo.</p>
            <a href="{{ route('catalogo') }}" class="inline-block bg-[var(--color-macuin-yellow)] text-black font-medium px-6 py-2.5 rounded-lg">Ir al catálogo</a>
        </div>
    @else
        <div class="grid lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2">
                <h1 class="text-2xl font-bold text-gray-900 mb-6">Carrito de compras</h1>
                <div class="space-y-4">
                    @foreach($carrito->lineas as $linea)
                        @php
                            $ap = $linea->autoparte;
                            $thumb = $ap?->imagen_url;
                            if ($thumb && !\Illuminate\Support\Str::startsWith($thumb, ['http://', 'https://'])) {
                                $thumb = asset(ltrim($thumb, '/'));
                            }
                        @endphp
                        <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-4 flex flex-col sm:flex-row sm:items-center gap-4">
                            <div class="shrink-0 w-full sm:w-24 h-32 sm:h-24 rounded-lg bg-gray-100 overflow-hidden flex items-center justify-center">
                                @if($thumb)
                                    <img src="{{ $thumb }}" alt="" class="w-full h-full object-cover">
                                @else
                                    <span class="text-gray-400 text-xs">Sin imagen</span>
                                @endif
                            </div>
                            <div class="flex-1">
                                <h3 class="font-medium text-gray-900">{{ $ap?->nombre ?? 'Producto' }}</h3>
                                <p class="text-sm text-gray-500">{{ $ap?->categoria?->nombre }} · SKU {{ $ap?->sku_codigo }}</p>
                                <div class="flex flex-wrap items-center gap-3 mt-3">
                                    <form method="post" action="{{ route('carrito.cantidad', $linea->id) }}" class="flex items-center gap-2">
                                        @csrf
                                        <label class="text-sm text-gray-600">Cant.</label>
                                        <input type="number" name="cantidad" value="{{ $linea->cantidad }}" min="1" max="999" class="w-20 rounded border-gray-300 text-sm">
                                        <button type="submit" class="text-sm text-amber-700 underline">Actualizar</button>
                                    </form>
                                    <form method="post" action="{{ route('carrito.quitar', $linea->id) }}" onsubmit="return confirm('¿Quitar este producto?');">
                                        @csrf
                                        <button type="submit" class="text-sm text-red-600 hover:underline">Quitar</button>
                                    </form>
                                </div>
                            </div>
                            <div class="text-right shrink-0 w-full sm:w-auto sm:min-w-[8rem]">
                                <p class="text-sm text-gray-500">Precio unit.</p>
                                <p class="font-semibold">${{ number_format((float) $linea->precio_unitario, 2, '.', ',') }}</p>
                                <p class="text-sm text-gray-500 mt-2">Subtotal</p>
                                <p class="font-bold text-gray-900">${{ number_format((float) $linea->precio_unitario * $linea->cantidad, 2, '.', ',') }}</p>
                            </div>
                        </div>
                    @endforeach
                </div>
            </div>
            <div class="lg:col-span-1">
                <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6 sticky top-4">
                    <h2 class="text-xl font-bold text-gray-900 mb-6">Resumen</h2>
                    <div class="space-y-3 mb-6 text-sm">
                        <div class="flex justify-between text-gray-600">
                            <span>Subtotal</span>
                            <span>${{ number_format($subtotal, 2, '.', ',') }}</span>
                        </div>
                        <div class="flex justify-between text-gray-600">
                            <span>Envío (fijo)</span>
                            <span>${{ number_format($envio, 2, '.', ',') }}</span>
                        </div>
                        <div class="flex justify-between text-lg font-bold text-gray-900 pt-3 border-t border-gray-200">
                            <span>Total</span>
                            <span class="text-amber-600">${{ number_format($total, 2, '.', ',') }}</span>
                        </div>
                    </div>
                    <a href="{{ route('pago') }}" class="block w-full text-center bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-semibold py-3 rounded-lg transition">Proceder al pago</a>
                </div>
            </div>
        </div>
    @endif
</div>
@endsection
