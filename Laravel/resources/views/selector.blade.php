<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MACUIN - Sistema de Gestión Automotriz</title>
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=instrument-sans:400,500,600,700" rel="stylesheet" />
    @if (file_exists(public_path('build/manifest.json')) || file_exists(public_path('hot')))
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    @else
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = { theme: { extend: { colors: { 'macuin-yellow': '#e5a00d', 'macuin-blue': '#2f546b' } } } };
        </script>
        <style>
            :root { --color-macuin-yellow: #e5a00d; --color-macuin-blue: #2f546b; }
        </style>
    @endif
</head>
<body class="bg-gray-50 min-h-screen flex flex-col items-center justify-center p-6">
    <div class="text-center mb-10">
        <div class="inline-flex items-center gap-1 bg-black text-[var(--color-macuin-yellow)] font-bold text-xl px-3 py-1 rounded mb-4">
            <span class="bg-[var(--color-macuin-yellow)] text-black px-1">M</span>MACUIN
        </div>
        <h1 class="text-4xl font-bold text-gray-900 mb-2">MACUIN</h1>
        <p class="text-gray-600">Robustez y Eficiencia</p>
        <p class="text-gray-500 text-sm">Sistema de Gestión Automotriz</p>
    </div>

    <div class="grid md:grid-cols-2 gap-8 max-w-4xl w-full">
        {{-- Cliente Externo --}}
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-8 flex flex-col">
            <div class="w-14 h-14 rounded-full bg-amber-100 flex items-center justify-center mx-auto mb-4">
                <svg class="w-7 h-7 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
            </div>
            <h2 class="text-xl font-semibold text-gray-900 mb-2">Cliente Externo</h2>
            <p class="text-gray-600 text-sm mb-4 flex-1">Acceso al catálogo de productos, carrito de compras, seguimiento de pedidos y gestión de cuenta personal.</p>
            <ul class="space-y-2 mb-6 text-sm text-gray-600">
                <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span> Ver catálogo de productos</li>
                <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span> Realizar pedidos en línea</li>
                <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span> Rastrear estado de órdenes</li>
                <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span> Contacto directo con soporte</li>
            </ul>
            <a href="{{ route('inicio') }}" class="block w-full bg-[var(--color-macuin-yellow)] hover:bg-amber-500 text-black font-semibold py-3 px-4 rounded-lg text-center transition">Entrar al portal de clientes</a>
            <p class="mt-4 text-center text-sm text-gray-600">
                <a href="{{ route('login') }}" class="text-amber-700 font-medium hover:underline">Iniciar sesión</a>
                <span class="mx-2 text-gray-300">|</span>
                <a href="{{ route('registro') }}" class="text-amber-700 font-medium hover:underline">Crear cuenta</a>
            </p>
        </div>

        {{-- Personal Interno --}}
        <div class="bg-white rounded-xl border-2 border-[var(--color-macuin-blue)] shadow-sm p-8 flex flex-col">
            <div class="w-14 h-14 rounded-full bg-slate-200 flex items-center justify-center mx-auto mb-4">
                <svg class="w-7 h-7 text-[var(--color-macuin-blue)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
            </div>
            <h2 class="text-xl font-semibold text-gray-900 mb-2">Personal Interno</h2>
            <p class="text-gray-600 text-sm mb-4 flex-1">Acceso al panel de gestión empresarial para equipos de Ventas, Almacén y Logística de MACUIN.</p>
            <ul class="space-y-2 mb-6 text-sm text-gray-600">
                <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[var(--color-macuin-blue)]"></span> Dashboard de métricas y KPIs</li>
                <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[var(--color-macuin-blue)]"></span> Gestión de inventario y stock</li>
                <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[var(--color-macuin-blue)]"></span> Administración de pedidos</li>
                <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[var(--color-macuin-blue)]"></span> Generación de reportes</li>
            </ul>
            <a href="{{ route('personal.login') }}" class="block w-full bg-[var(--color-macuin-blue)] hover:opacity-90 text-white font-semibold py-3 px-4 rounded-lg text-center transition">Acceso Personal</a>
        </div>
    </div>

    <footer class="mt-12 text-center text-sm text-gray-500">
        <p>Sistema Protegido - Solo para usuarios autorizados</p>
        <p class="mt-1">© {{ date('Y') }} MACUIN. Todos los derechos reservados.</p>
    </footer>
</body>
</html>
