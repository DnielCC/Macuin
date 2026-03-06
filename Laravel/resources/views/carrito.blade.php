@extends('layouts.app')

@section('title', 'Carrito de Compras')

@section('content')
<div class="container mx-auto px-4 py-8">
    <div class="flex justify-end mb-6">
        <a href="{{ route('catalogo') }}" class="text-amber-600 hover:underline font-medium">Continuar Comprando</a>
    </div>

    <div class="grid lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2">
            <h1 class="text-2xl font-bold text-gray-900 mb-6">Carrito de Compras</h1>
            <div class="space-y-4">
                @php
                    $items = [
                        ['nombre' => 'Filtro de Aceite Premium', 'categoria' => 'Filtros', 'cantidad' => 2, 'precio' => 25000],
                        ['nombre' => 'Pastillas de Freno', 'categoria' => 'Frenos', 'cantidad' => 1, 'precio' => 45000],
                        ['nombre' => 'Amortiguador Delantero', 'categoria' => 'Suspensión', 'cantidad' => 1, 'precio' => 125000],
                    ];
                    $subtotal = 195000;
                    $envio = 5000;
                    $total = 200000;
                @endphp
                @foreach($items as $item)
                    <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-4 flex flex-col sm:flex-row sm:items-center gap-4">
                        <div class="flex-1">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h3 class="font-medium text-gray-900">{{ $item['nombre'] }}</h3>
                                    <p class="text-sm text-gray-500">{{ $item['categoria'] }}</p>
                                </div>
                                <button type="button" class="text-red-500 hover:text-red-600 p-1" title="Eliminar">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                                </button>
                            </div>
                            <div class="flex items-center gap-4 mt-2 sm:mt-0 sm:flex-1 sm:justify-end">
                                <div class="flex items-center border border-gray-300 rounded-lg overflow-hidden">
                                    <button type="button" class="px-3 py-1.5 hover:bg-gray-100">−</button>
                                    <input type="number" value="{{ $item['cantidad'] }}" min="1" class="w-12 text-center border-0 border-x border-gray-300 py-1.5 text-sm">
                                    <button type="button" class="px-3 py-1.5 hover:bg-gray-100">+</button>
                                </div>
                                <span class="font-semibold text-gray-900">${{ number_format($item['precio'] * $item['cantidad'], 0, ',', '.') }}</span>
                            </div>
                        </div>
                    </div>
                @endforeach
            </div>
        </div>
        <div class="lg:col-span-1">
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6 sticky top-4">
                <h2 class="text-xl font-bold text-gray-900 mb-6">Resumen del Pedido</h2>
                <div class="space-y-3 mb-6">
                    <div class="flex justify-between text-gray-600">
                        <span>Subtotal</span>
                        <span>${{ number_format($subtotal, 0, ',', '.') }}</span>
                    </div>
                    <div class="flex justify-between text-gray-600">
                        <span>Envío</span>
                        <span>${{ number_format($envio, 0, ',', '.') }}</span>
                    </div>
                    <div class="flex justify-between text-lg font-bold text-gray-900 pt-3 border-t border-gray-200">
                        <span>Total</span>
                        <span class="text-amber-600">${{ number_format($total, 0, ',', '.') }}</span>
                    </div>
                </div>
                <a href="{{ route('pago') }}" class="block w-full bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-semibold py-3 rounded-lg text-center uppercase text-sm tracking-wide transition">
                    Proceder al pago
                </a>
            </div>
        </div>
    </div>
</div>
@endsection
