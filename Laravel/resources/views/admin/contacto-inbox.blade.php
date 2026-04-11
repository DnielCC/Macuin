@extends('layouts.app')

@section('title', 'Bandeja de contacto')

@section('content')
<div class="container mx-auto px-4 py-8">
    <div class="flex flex-wrap justify-between items-center gap-4 mb-6">
        <div>
            <h1 class="text-2xl font-bold text-gray-900">Mensajes de contacto</h1>
            <p class="text-sm text-gray-600">Sin leer: <strong>{{ $sinLeer }}</strong></p>
        </div>
        <a href="{{ route('inicio') }}" class="text-amber-700 hover:underline text-sm">Volver al inicio</a>
    </div>

    <div class="overflow-x-auto rounded-xl border border-gray-100 bg-white shadow-sm">
        <table class="min-w-full text-sm">
            <thead class="bg-gray-50 text-left text-gray-600">
                <tr>
                    <th class="px-4 py-3">#</th>
                    <th class="px-4 py-3">Fecha</th>
                    <th class="px-4 py-3">De</th>
                    <th class="px-4 py-3">Asunto</th>
                    <th class="px-4 py-3">Estado</th>
                    <th class="px-4 py-3"></th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                @forelse($mensajes as $m)
                    <tr class="{{ $m->is_read ? '' : 'bg-amber-50/50' }}">
                        <td class="px-4 py-3">{{ $m->id }}</td>
                        <td class="px-4 py-3 text-gray-500 whitespace-nowrap">{{ $m->created_at->format('d/m/Y H:i') }}</td>
                        <td class="px-4 py-3">
                            <div class="font-medium text-gray-900">{{ $m->name }}</div>
                            <div class="text-xs text-gray-500">{{ $m->email }}</div>
                            @if($m->phone)<div class="text-xs text-gray-400">{{ $m->phone }}</div>@endif
                        </td>
                        <td class="px-4 py-3 max-w-xs truncate" title="{{ $m->subject }}">{{ $m->subject }}</td>
                        <td class="px-4 py-3">
                            @if($m->is_read)
                                <span class="text-xs text-gray-500">Leído</span>
                            @else
                                <span class="text-xs font-semibold text-amber-800">Nuevo</span>
                            @endif
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap">
                            <button type="button" class="text-amber-700 hover:underline text-xs mr-2" onclick="document.getElementById('msg-{{ $m->id }}').classList.toggle('hidden')">Ver</button>
                            @if(!$m->is_read)
                                <form method="post" action="{{ route('admin.contacto.leido', $m) }}" class="inline">@csrf
                                    <button type="submit" class="text-gray-600 hover:underline text-xs">Marcar leído</button>
                                </form>
                            @endif
                        </td>
                    </tr>
                    <tr id="msg-{{ $m->id }}" class="hidden bg-gray-50">
                        <td colspan="6" class="px-4 py-4 text-gray-700 whitespace-pre-wrap">{{ $m->message }}</td>
                    </tr>
                @empty
                    <tr><td colspan="6" class="px-4 py-8 text-center text-gray-500">No hay mensajes.</td></tr>
                @endforelse
            </tbody>
        </table>
    </div>
</div>
@endsection
