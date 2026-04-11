@extends('layouts.app')

@section('title', 'Pago simulado')

@section('content')
<div class="container mx-auto px-4 py-8 max-w-3xl">
    <h1 class="text-2xl font-bold text-gray-900 mb-2">Checkout</h1>
    <p class="text-gray-600 text-sm mb-6">Envío + dirección de entrega + pasarela <strong>simulada</strong> (no cobra tarjetas reales).</p>

    <div class="rounded-lg bg-amber-50 border border-amber-200 text-amber-900 text-sm px-4 py-3 mb-6">
        <strong>Demo:</strong> para aprobar el pago usa una tarjeta de <strong>16 dígitos «4»</strong> (4444444444444444). Cualquier otra combinación de 16 dígitos será rechazada en esta simulación.
    </div>

    <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6">
        <h2 class="font-semibold text-gray-900 mb-3">Tu pedido</h2>
        <ul class="text-sm text-gray-600 space-y-1 mb-4">
            @foreach($carrito->lineas as $ln)
                <li>{{ $ln->autoparte?->nombre }} × {{ $ln->cantidad }} — ${{ number_format((float) $ln->precio_unitario * $ln->cantidad, 2, '.', ',') }}</li>
            @endforeach
        </ul>
        <div class="flex justify-between text-sm border-t pt-3">
            <span>Subtotal</span><span>${{ number_format($subtotal, 2, '.', ',') }}</span>
        </div>
        <div class="flex justify-between text-sm">
            <span>Envío</span><span>${{ number_format($envio, 2, '.', ',') }}</span>
        </div>
        <div class="flex justify-between font-bold text-gray-900 mt-2">
            <span>Total</span><span class="text-amber-600">${{ number_format($total, 2, '.', ',') }}</span>
        </div>
    </div>

    <form method="post" action="{{ route('pago.procesar') }}" id="form-pago" class="space-y-6 bg-white rounded-xl border border-gray-100 shadow-sm p-6">
        @csrf
        <h2 class="font-semibold text-gray-900">Dirección de envío</h2>
        <div class="grid sm:grid-cols-2 gap-4">
            <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-gray-700">Calle y número (calle)</label>
                <input name="calle_principal" value="{{ old('calle_principal', auth()->user()->address) }}" required maxlength="150" class="mt-1 w-full rounded-lg border-gray-300 @error('calle_principal') border-red-500 @enderror">
                @error('calle_principal')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Núm. exterior</label>
                <input name="num_ext" value="{{ old('num_ext') }}" required maxlength="10" class="mt-1 w-full rounded-lg border-gray-300">
                @error('num_ext')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Núm. interior</label>
                <input name="num_int" value="{{ old('num_int') }}" maxlength="10" class="mt-1 w-full rounded-lg border-gray-300">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Colonia</label>
                <input name="colonia" value="{{ old('colonia') }}" required maxlength="100" class="mt-1 w-full rounded-lg border-gray-300">
                @error('colonia')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Municipio / Ciudad</label>
                <input name="municipio" value="{{ old('municipio') }}" required maxlength="100" class="mt-1 w-full rounded-lg border-gray-300">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Estado</label>
                <input name="estado" value="{{ old('estado') }}" required maxlength="100" class="mt-1 w-full rounded-lg border-gray-300">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">C.P.</label>
                <input name="cp" value="{{ old('cp') }}" required pattern="\d{4,5}" maxlength="5" class="mt-1 w-full rounded-lg border-gray-300" placeholder="01000">
                @error('cp')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
            </div>
            <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-gray-700">Referencias (opcional)</label>
                <input name="referencias" value="{{ old('referencias') }}" maxlength="500" class="mt-1 w-full rounded-lg border-gray-300">
            </div>
        </div>

        <h2 class="font-semibold text-gray-900 pt-2">Tarjeta (simulación)</h2>
        <div class="grid sm:grid-cols-2 gap-4">
            <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-gray-700">Titular</label>
                <input name="titular_tarjeta" value="{{ old('titular_tarjeta', auth()->user()->name) }}" required maxlength="120" class="mt-1 w-full rounded-lg border-gray-300">
                @error('titular_tarjeta')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
            </div>
            <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-gray-700">Número (16 dígitos)</label>
                <input name="numero_tarjeta" value="{{ old('numero_tarjeta') }}" required inputmode="numeric" autocomplete="off" maxlength="19" class="mt-1 w-full rounded-lg border-gray-300 font-mono" placeholder="4444444444444444">
                @error('numero_tarjeta')<p class="text-red-600 text-xs mt-1">{{ $message }}</p>@enderror
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Vencimiento (MM/AA)</label>
                <input name="expira" value="{{ old('expira') }}" maxlength="7" class="mt-1 w-full rounded-lg border-gray-300" placeholder="12/28">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">CVV</label>
                <input name="cvv" type="password" value="{{ old('cvv') }}" maxlength="4" class="mt-1 w-full rounded-lg border-gray-300" placeholder="123">
            </div>
        </div>

        <div id="pago-loading" class="hidden text-sm text-gray-600 flex items-center gap-2">
            <svg class="animate-spin h-5 w-5 text-amber-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            Procesando pago…
        </div>

        <button type="submit" id="btn-pagar" class="w-full py-3 rounded-lg bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-semibold transition">
            Pagar ${{ number_format($total, 2, '.', ',') }} MXN
        </button>
    </form>
</div>
@push('scripts')
<script>
document.getElementById('form-pago')?.addEventListener('submit', function () {
    document.getElementById('pago-loading')?.classList.remove('hidden');
    document.getElementById('btn-pagar')?.setAttribute('disabled', 'disabled');
});
</script>
@endpush
@endsection
