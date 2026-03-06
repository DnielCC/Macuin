<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title', 'MACUIN') - {{ config('app.name') }}</title>
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=instrument-sans:400,500,600,700" rel="stylesheet" />
    @if (file_exists(public_path('build/manifest.json')) || file_exists(public_path('hot')))
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    @else
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
                theme: { extend: { colors: { 'macuin-yellow': '#e5a00d', 'macuin-blue': '#2f546b' } } }
            };
        </script>
        <style>
            :root { --color-macuin-yellow: #e5a00d; --color-macuin-yellow-light: #f5c542; --color-macuin-blue: #2f546b; --color-macuin-dark: #1a1a1a; }
        </style>
    @endif
    @stack('styles')
</head>
<body class="bg-gray-50 text-gray-800 antialiased min-h-screen flex flex-col">
    @hasSection('no-header')
        @yield('content')
    @else
        @include('layouts.partials.header')
        <main class="flex-1">
            @yield('content')
        </main>
        @include('layouts.partials.footer')
    @endif
    @stack('scripts')
</body>
</html>
