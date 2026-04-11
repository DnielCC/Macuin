@extends('layouts.app')

@section('title', 'Mi Cuenta')

@section('content')
<section class="container mx-auto px-4 py-12">
    <div class="max-w-5xl mx-auto">
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
                <a href="/catalogo" class="inline-flex items-center justify-center rounded-lg bg-[var(--color-macuin-yellow)] px-5 py-3 text-sm font-semibold text-black hover:bg-amber-500 transition">
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

        <div class="mt-10 bg-white rounded-xl border border-gray-100 shadow-sm p-6 md:p-8">
            <h2 class="text-xl font-bold text-gray-900 mb-2">Mensajes de contacto</h2>
            <p class="text-sm text-gray-500 mb-6">Consultas que enviaste desde el formulario de contacto. Aquí ves el estado y las respuestas del equipo Macuin.</p>

            @if ($mensajesContacto->isEmpty())
                <p class="text-sm text-gray-600">Aún no hay mensajes asociados a tu correo o cuenta.</p>
            @else
                <div class="overflow-x-auto rounded-lg border border-gray-200">
                    <table class="min-w-full text-sm text-left">
                        <thead class="bg-gray-50 text-gray-600 font-semibold border-b border-gray-200">
                            <tr>
                                <th class="px-4 py-3 whitespace-nowrap">Fecha</th>
                                <th class="px-4 py-3">Asunto</th>
                                <th class="px-4 py-3 whitespace-nowrap">Estado</th>
                                <th class="px-4 py-3">Tu mensaje</th>
                                <th class="px-4 py-3">Respuesta del equipo</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            @foreach ($mensajesContacto as $msg)
                                @php
                                    $reply = trim((string) ($msg->admin_reply ?? ''));
                                    $estado = $reply !== '' ? 'Contestado' : ($msg->is_read ? 'Leído' : 'No leído');
                                    $badgeClass = $reply !== ''
                                        ? 'bg-green-100 text-green-800 border border-green-200'
                                        : ($msg->is_read
                                            ? 'bg-gray-100 text-gray-800 border border-gray-200'
                                            : 'bg-amber-100 text-amber-900 border border-amber-200');
                                @endphp
                                <tr class="align-top hover:bg-gray-50/80">
                                    <td class="px-4 py-3 text-gray-600 whitespace-nowrap">
                                        {{ $msg->created_at?->format('Y-m-d H:i') ?? '—' }}
                                    </td>
                                    <td class="px-4 py-3 font-medium text-gray-900">{{ $msg->subject }}</td>
                                    <td class="px-4 py-3">
                                        <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium {{ $badgeClass }}">
                                            {{ $estado }}
                                        </span>
                                    </td>
                                    <td class="px-4 py-3 text-gray-700 max-w-xs">
                                        {{ \Illuminate\Support\Str::limit($msg->message, 120) }}
                                    </td>
                                    <td class="px-4 py-3 text-gray-700 max-w-md">
                                        @if ($reply !== '')
                                            <span class="text-gray-900">{{ $reply }}</span>
                                            @if ($msg->replied_at)
                                                <p class="text-xs text-gray-500 mt-1">Respondido: {{ $msg->replied_at->format('Y-m-d H:i') }}</p>
                                            @endif
                                        @else
                                            <span class="text-gray-400">—</span>
                                        @endif
                                    </td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            @endif
        </div>
    </div>
</section>
@endsection
