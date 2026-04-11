@extends('layouts.app')

@section('title', 'Mis pedidos')

@section('content')
<div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-2">Mis pedidos</h1>
    <p class="text-gray-600 text-sm mb-8">Pedidos asociados a tu correo en la tabla <code class="text-xs">clientes</code> de la base de datos.</p>

    @if($pedidos->isEmpty())
        <div class="rounded-xl border border-gray-200 bg-white p-10 text-center text-gray-600">
            <p>Aún no tienes pedidos registrados.</p>
            <p class="text-sm mt-2">Tras completar un pago desde el carrito, aparecerán aquí.</p>
            <a href="{{ route('catalogo') }}" class="inline-block mt-4 text-amber-700 font-medium hover:underline">Ir al catálogo</a>
        </div>
    @else
        <div class="overflow-x-auto rounded-xl border border-gray-100 bg-white shadow-sm">
            <table class="min-w-full text-sm">
                <thead class="bg-gray-50 text-left text-gray-600">
                    <tr>
                        <th class="px-4 py-3">#</th>
                        <th class="px-4 py-3">Folio</th>
                        <th class="px-4 py-3">Total</th>
                        <th class="px-4 py-3">Estatus</th>
                        <th class="px-4 py-3">Fecha</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                    @foreach($pedidos as $ped)
                        <tr>
                            <td class="px-4 py-3 font-medium">{{ $ped->id }}</td>
                            <td class="px-4 py-3 text-gray-600">{{ $ped->folio ?? '—' }}</td>
                            <td class="px-4 py-3">${{ number_format((float) $ped->total, 2, '.', ',') }}</td>
                            <td class="px-4 py-3">
                                <span class="inline-flex rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-800">{{ $ped->estatus?->nombre ?? '—' }}</span>
                            </td>
                            <td class="px-4 py-3 text-gray-500">
                                @php $fp = $ped->fecha_pedido; @endphp
                                @if($fp)
                                    {{ $fp->timezone(config('app.timezone'))->format('d/m/Y H:i') }}
                                @else
                                    —
                                @endif
                            </td>
                        </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
    @endif
</div>
@endsection
