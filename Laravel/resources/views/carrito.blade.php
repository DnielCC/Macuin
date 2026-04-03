@extends('layouts.app')

@section('title', 'Carrito de Compras')

@section('content')
<div class="container mx-auto px-4 py-8">
    <div class="flex justify-end mb-6">
        <a href="/catalogo" class="text-amber-600 hover:underline font-medium">Continuar Comprando</a>
    </div>

    <div class="mb-6 max-w-3xl mx-auto rounded-lg border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-600 text-center">
        Vista estática de demostración: sin carrito real ni checkout.
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
                                <span class="text-gray-300 p-1 inline-flex" title="Solo maquetación" aria-hidden="true">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                                </span>
                            </div>
                            <div class="flex items-center gap-4 mt-2 sm:mt-0 sm:flex-1 sm:justify-end">
                                <div class="flex items-center border border-gray-200 rounded-lg bg-gray-50 px-3 py-1.5 text-sm text-gray-600">
                                    Cantidad: <span class="ml-1 font-medium text-gray-900">{{ $item['cantidad'] }}</span>
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
                <span class="block w-full bg-gray-200 text-gray-500 font-semibold py-3 rounded-lg text-center uppercase text-sm tracking-wide cursor-default">
                    Proceder al pago
                </span>
            </div>
        </div>
    </div>
</div>
@endsection
