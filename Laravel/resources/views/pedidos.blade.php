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
                        <th class="px-4 py-3 text-center">Acciones</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                    @foreach($pedidos as $ped)
                        @php
                            $nombreEstatus = $ped->estatus?->nombre ?? '—';
                            $colorEstatus  = $ped->estatus?->color ?? '#94a3b8';
                            $yaCancelado   = !empty($ped->motivo_cancelacion);
                            $estatusNoCancelables = ['Enviado', 'Entregado', 'Cancelado'];
                            $puedeCancelar = !$yaCancelado && !in_array($nombreEstatus, $estatusNoCancelables, true);
                        @endphp
                        <tr>
                            <td class="px-4 py-3 font-medium">{{ $ped->id }}</td>
                            <td class="px-4 py-3 text-gray-600">{{ $ped->folio ?? '—' }}</td>
                            <td class="px-4 py-3">${{ number_format((float) $ped->total, 2, '.', ',') }}</td>
                            <td class="px-4 py-3">
                                <span class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium"
                                      style="background-color: {{ $colorEstatus }}20; color: {{ $colorEstatus }}; border: 1px solid {{ $colorEstatus }}40;">
                                    <span class="inline-block w-1.5 h-1.5 rounded-full" style="background-color: {{ $colorEstatus }};"></span>
                                    {{ $nombreEstatus }}
                                </span>
                                @if($yaCancelado)
                                    <p class="text-xs text-red-500 mt-1 max-w-[200px] truncate" title="{{ $ped->motivo_cancelacion }}">
                                        Motivo: {{ $ped->motivo_cancelacion }}
                                    </p>
                                @endif
                            </td>
                            <td class="px-4 py-3 text-gray-500">
                                @php $fp = !empty($ped->fecha_pedido) ? \Illuminate\Support\Carbon::parse($ped->fecha_pedido) : null; @endphp
                                @if($fp)
                                    {{ $fp->timezone(config('app.timezone', 'UTC'))->format('d/m/Y H:i') }}
                                @else
                                    —
                                @endif
                            </td>
                            <td class="px-4 py-3 text-center">
                                @if($puedeCancelar)
                                    <button type="button"
                                            onclick="abrirModalCancelar({{ $ped->id }}, '{{ $ped->folio ?? $ped->id }}')"
                                            class="inline-flex items-center gap-1 rounded-lg border border-red-200 bg-red-50 px-3 py-1.5 text-xs font-medium text-red-700 transition hover:bg-red-100 hover:border-red-300 focus:outline-none focus:ring-2 focus:ring-red-300">
                                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                  d="M6 18L18 6M6 6l12 12"/>
                                        </svg>
                                        Cancelar
                                    </button>
                                @elseif($yaCancelado)
                                    <span class="text-xs text-gray-400 italic">Cancelado</span>
                                @else
                                    <span class="text-xs text-gray-400">—</span>
                                @endif
                            </td>
                        </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
    @endif
</div>

{{-- Modal de confirmación de cancelación --}}
<div id="modal-cancelar" class="fixed inset-0 z-50 hidden">
    {{-- Overlay --}}
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity" onclick="cerrarModalCancelar()"></div>

    {{-- Panel --}}
    <div class="relative flex items-center justify-center min-h-screen px-4">
        <div class="relative w-full max-w-md rounded-2xl bg-white shadow-2xl ring-1 ring-gray-900/5 p-6 animate-[fadeInUp_.25s_ease]">
            <button type="button" onclick="cerrarModalCancelar()"
                    class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>

            <div class="flex items-center gap-3 mb-4">
                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-red-100">
                    <svg class="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                </div>
                <div>
                    <h3 class="text-lg font-semibold text-gray-900">Cancelar pedido</h3>
                    <p class="text-sm text-gray-500">Pedido <strong id="modal-pedido-ref"></strong></p>
                </div>
            </div>

            <form id="form-cancelar" method="POST" action="">
                @csrf
                <label for="motivo_cancelacion" class="block text-sm font-medium text-gray-700 mb-1">
                    Motivo de cancelación <span class="text-red-500">*</span>
                </label>
                <textarea id="motivo_cancelacion" name="motivo_cancelacion" rows="3" required minlength="3" maxlength="2000"
                          placeholder="Describe brevemente por qué deseas cancelar este pedido…"
                          class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-800 placeholder-gray-400 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition resize-none"></textarea>
                <p class="text-xs text-gray-400 mt-1">Mínimo 3 caracteres.</p>

                <div class="mt-5 flex items-center justify-end gap-3">
                    <button type="button" onclick="cerrarModalCancelar()"
                            class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50">
                        Volver
                    </button>
                    <button type="submit"
                            class="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700 focus:ring-2 focus:ring-red-300">
                        Confirmar cancelación
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

@push('styles')
<style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
</style>
@endpush

@push('scripts')
<script>
    function abrirModalCancelar(pedidoId, folio) {
        var modal = document.getElementById('modal-cancelar');
        var form  = document.getElementById('form-cancelar');
        var ref   = document.getElementById('modal-pedido-ref');
        form.action = '/pedidos/' + pedidoId + '/cancelar';
        ref.textContent = '#' + folio;
        document.getElementById('motivo_cancelacion').value = '';
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
    function cerrarModalCancelar() {
        var modal = document.getElementById('modal-cancelar');
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
    // Cerrar con Escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') cerrarModalCancelar();
    });
</script>
@endpush
@endsection
