@extends('layouts.app')

@section('title', 'Mi Cuenta')

@section('content')
<section class="container mx-auto px-4 py-12">
    <div class="max-w-3xl mx-auto">
        @if (session('status'))
            <div class="mb-6 rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
                {{ session('status') }}
            </div>
        @endif

        <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-8">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
                <div>
                    <p class="text-sm uppercase tracking-wide text-amber-600 font-semibold">Portal de clientes</p>
                    <h1 class="text-3xl font-bold text-gray-900">Bienvenido, {{ auth()->user()->name }}</h1>
                    <p class="text-gray-500 mt-2">Tu cuenta ya se encuentra activa y lista para las siguientes etapas del sistema.</p>
                </div>
                <a href="{{ route('catalogo') }}" class="inline-flex items-center justify-center rounded-lg bg-[var(--color-macuin-yellow)] px-5 py-3 text-sm font-semibold text-black hover:bg-amber-500 transition">
                    Ir al catálogo
                </a>
            </div>

            <div class="grid md:grid-cols-2 gap-6">
                <div class="rounded-xl border border-gray-200 p-5">
                    <h2 class="text-lg font-semibold text-gray-900 mb-4">Datos principales</h2>
                    <dl class="space-y-3 text-sm text-gray-700">
                        <div>
                            <dt class="font-medium text-gray-500">Nombre</dt>
                            <dd>{{ auth()->user()->name }}</dd>
                        </div>
                        <div>
                            <dt class="font-medium text-gray-500">Correo electrónico</dt>
                            <dd>{{ auth()->user()->email }}</dd>
                        </div>
                        <div>
                            <dt class="font-medium text-gray-500">Teléfono</dt>
                            <dd>{{ auth()->user()->phone ?: 'No registrado' }}</dd>
                        </div>
                    </dl>
                </div>

                <div class="rounded-xl border border-gray-200 p-5">
                    <h2 class="text-lg font-semibold text-gray-900 mb-4">Datos comerciales</h2>
                    <dl class="space-y-3 text-sm text-gray-700">
                        <div>
                            <dt class="font-medium text-gray-500">Empresa</dt>
                            <dd>{{ auth()->user()->company ?: 'No registrada' }}</dd>
                        </div>
                        <div>
                            <dt class="font-medium text-gray-500">Dirección</dt>
                            <dd>{{ auth()->user()->address ?: 'No registrada' }}</dd>
                        </div>
                        <div>
                            <dt class="font-medium text-gray-500">Estado de cuenta</dt>
                            <dd>Activa</dd>
                        </div>
                    </dl>
                </div>
            </div>
        </div>
    </div>
</section>
@endsection
