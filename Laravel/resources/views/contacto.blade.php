@extends('layouts.app')

@section('title', 'Contáctanos')

@section('content')
<div class="container mx-auto px-4 py-12">
    <div class="flex flex-col lg:flex-row justify-between gap-4 mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Contáctanos</h1>
        <a href="{{ route('catalogo') }}" class="text-amber-600 hover:underline font-medium">Volver al catálogo</a>
    </div>
    <p class="text-gray-600 mb-10">Estamos aquí para ayudarte con tus necesidades automotrices.</p>

    <div class="grid lg:grid-cols-3 gap-8 lg:gap-10 items-start">
        {{-- Panel izquierdo (estructura original) --}}
        <div class="lg:col-span-1 space-y-4">
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <div class="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center mb-3">
                    <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Teléfono</h3>
                <p class="text-gray-600 text-sm">+52 55 1234 5678</p>
                <p class="text-gray-600 text-sm">+52 55 8765 4321</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <div class="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center mb-3">
                    <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Email</h3>
                <p class="text-gray-600 text-sm">ventas@macuin.com</p>
                <p class="text-gray-600 text-sm">soporte@macuin.com</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <div class="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center mb-3">
                    <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Dirección</h3>
                <p class="text-gray-600 text-sm">Av. Industrial #1234</p>
                <p class="text-gray-600 text-sm">Col. Zona Industrial</p>
                <p class="text-gray-600 text-sm">Ciudad de México, 01234</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <div class="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center mb-3">
                    <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <h3 class="font-semibold text-gray-900 mb-2">Horario de atención</h3>
                <p class="text-gray-600 text-sm">Lunes - Viernes: 8:00 - 18:00</p>
                <p class="text-gray-600 text-sm">Sábado: 9:00 - 14:00</p>
                <p class="text-gray-600 text-sm">Domingo: Cerrado</p>
            </div>
        </div>

        {{-- Formulario en rejilla (más horizontal, menos alto) --}}
        <div class="lg:col-span-2 flex justify-center lg:justify-end">
            <div class="w-full max-w-xl rounded-2xl border border-gray-200/90 bg-white shadow-sm ring-1 ring-gray-900/[0.04] p-5 sm:p-6">
                <h2 class="text-base font-semibold text-gray-900 tracking-tight">Envíanos un mensaje</h2>
                <p class="text-gray-500 text-[11px] mt-0.5 mb-3 leading-snug">Te responderemos pronto; tu mensaje queda registrado para nuestro equipo.</p>

                <form method="post" action="{{ route('contacto.store') }}" class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-2.5">
                    @csrf
                    <div class="min-w-0">
                        <label for="contact-name" class="block text-[11px] font-medium text-gray-500 uppercase tracking-wide">Nombre</label>
                        <input id="contact-name" type="text" name="name" value="{{ old('name', auth()->user()?->name) }}" required maxlength="200" placeholder="Tu nombre"
                               class="mt-0.5 w-full rounded-lg border-gray-200 bg-gray-50/50 px-2.5 py-1.5 text-sm text-gray-900 placeholder:text-gray-400 focus:border-amber-400 focus:bg-white focus:ring-1 focus:ring-amber-400 @error('name') border-red-400 ring-1 ring-red-200 @enderror">
                        @error('name')<p class="text-red-600 text-[11px] mt-0.5">{{ $message }}</p>@enderror
                    </div>
                    <div class="min-w-0">
                        <label for="contact-email" class="block text-[11px] font-medium text-gray-500 uppercase tracking-wide">Correo</label>
                        <input id="contact-email" type="email" name="email" value="{{ old('email', auth()->user()?->email) }}" required maxlength="255" placeholder="correo@ejemplo.com"
                               class="mt-0.5 w-full rounded-lg border-gray-200 bg-gray-50/50 px-2.5 py-1.5 text-sm focus:border-amber-400 focus:bg-white focus:ring-1 focus:ring-amber-400 @error('email') border-red-400 ring-1 ring-red-200 @enderror">
                        @error('email')<p class="text-red-600 text-[11px] mt-0.5">{{ $message }}</p>@enderror
                    </div>
                    <div class="min-w-0">
                        <label for="contact-phone" class="block text-[11px] font-medium text-gray-500 uppercase tracking-wide">Teléfono <span class="normal-case font-normal text-gray-400">(opc.)</span></label>
                        <input id="contact-phone" type="text" name="phone" value="{{ old('phone', auth()->user()?->phone) }}" maxlength="40" placeholder="+52 …"
                               class="mt-0.5 w-full rounded-lg border-gray-200 bg-gray-50/50 px-2.5 py-1.5 text-sm focus:border-amber-400 focus:bg-white focus:ring-1 focus:ring-amber-400">
                        @error('phone')<p class="text-red-600 text-[11px] mt-0.5">{{ $message }}</p>@enderror
                    </div>
                    <div class="min-w-0">
                        <label for="contact-subject" class="block text-[11px] font-medium text-gray-500 uppercase tracking-wide">Asunto</label>
                        <input id="contact-subject" type="text" name="subject" value="{{ old('subject') }}" required maxlength="200" placeholder="Consulta breve"
                               class="mt-0.5 w-full rounded-lg border-gray-200 bg-gray-50/50 px-2.5 py-1.5 text-sm focus:border-amber-400 focus:bg-white focus:ring-1 focus:ring-amber-400 @error('subject') border-red-400 ring-1 ring-red-200 @enderror">
                        @error('subject')<p class="text-red-600 text-[11px] mt-0.5">{{ $message }}</p>@enderror
                    </div>
                    <div class="sm:col-span-2 min-w-0">
                        <label for="contact-message" class="block text-[11px] font-medium text-gray-500 uppercase tracking-wide">Mensaje</label>
                        <textarea id="contact-message" name="message" rows="3" required maxlength="5000" placeholder="Escribe tu mensaje…"
                                  class="mt-0.5 w-full resize-y min-h-[4.25rem] max-h-32 rounded-lg border-gray-200 bg-gray-50/50 px-2.5 py-1.5 text-sm leading-snug focus:border-amber-400 focus:bg-white focus:ring-1 focus:ring-amber-400 @error('message') border-red-400 ring-1 ring-red-200 @enderror">{{ old('message') }}</textarea>
                        @error('message')<p class="text-red-600 text-[11px] mt-0.5">{{ $message }}</p>@enderror
                    </div>
                    <div class="sm:col-span-2 flex justify-stretch sm:justify-end pt-0.5">
                        <button type="submit" class="w-full sm:w-auto min-w-[10rem] rounded-lg bg-[var(--color-macuin-yellow)] px-5 py-2 text-sm font-semibold text-black shadow-sm transition hover:bg-amber-500">
                            Enviar mensaje
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
@endsection
