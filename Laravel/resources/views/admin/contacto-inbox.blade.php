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

    @if (session('status'))
        <div class="mb-4 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">{{ session('status') }}</div>
    @endif

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
                            @if($m->admin_reply)
                                <span class="text-xs text-emerald-700 font-medium">Respondido</span>
                            @elseif($m->is_read)
                                <span class="text-xs text-gray-500">Leído</span>
                            @else
                                <span class="text-xs font-semibold text-amber-800">Nuevo</span>
                            @endif
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap">
                            <button type="button" class="text-amber-700 hover:underline text-xs mr-2" onclick="document.getElementById('msg-{{ $m->id }}').classList.toggle('hidden')">Ver / responder</button>
                            @if(!$m->is_read)
                                <form method="post" action="{{ route('admin.contacto.leido', $m) }}" class="inline">@csrf
                                    <button type="submit" class="text-gray-600 hover:underline text-xs">Solo marcar leído</button>
                                </form>
                            @endif
                        </td>
                    </tr>
                    <tr id="msg-{{ $m->id }}" class="hidden bg-gray-50">
                        <td colspan="6" class="px-4 py-4">
                            <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Mensaje del cliente</p>
                            <div class="text-gray-800 whitespace-pre-wrap mb-4 border-b border-gray-200 pb-4">{{ $m->message }}</div>

                            @if($m->admin_reply)
                                <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Tu respuesta registrada ({{ optional($m->replied_at)->format('d/m/Y H:i') }})</p>
                                <div class="text-gray-800 whitespace-pre-wrap mb-4 p-3 rounded-lg bg-white border border-gray-200">{{ $m->admin_reply }}</div>
                            @endif

                            @php
                                $cuerpoCorreo = "Hola {$m->name},\n\n".($m->admin_reply ?: '')."\n\n— Equipo MACUIN";
                                $mailto = 'mailto:'.rawurlencode($m->email).'?subject='.rawurlencode('Re: '.$m->subject).'&body='.rawurlencode($cuerpoCorreo);
                            @endphp
                            <a href="{{ $mailto }}" class="inline-block text-sm font-medium text-amber-800 hover:underline mb-4">Abrir cliente de correo para enviar al cliente</a>

                            <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Guardar o actualizar respuesta (texto interno + plantilla para el correo)</p>
                            <form method="post" action="{{ route('admin.contacto.responder', $m) }}" class="space-y-2 max-w-2xl" onsubmit="var b=this.querySelector('button[type=submit]'); if(b){ b.disabled=true; b.textContent='Guardando…'; }">
                                @csrf
                                <textarea name="reply_{{ $m->id }}" rows="5" required maxlength="5000" class="w-full rounded-lg border-gray-300 text-sm" placeholder="Escribe aquí la respuesta al cliente…">{{ old('reply_'.$m->id, $m->admin_reply) }}</textarea>
                                <button type="submit" class="rounded-lg bg-[var(--color-macuin-yellow)] px-4 py-2 text-sm font-semibold text-black hover:bg-amber-500">Guardar respuesta</button>
                            </form>
                        </td>
                    </tr>
                @empty
                    <tr><td colspan="6" class="px-4 py-8 text-center text-gray-500">No hay mensajes.</td></tr>
                @endforelse
            </tbody>
        </table>
    </div>
</div>
@endsection
