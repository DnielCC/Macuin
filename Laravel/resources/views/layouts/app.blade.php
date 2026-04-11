<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
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
            @keyframes macuin-cart-bump { 0%,100%{transform:translateY(0)} 25%{transform:translateY(-10px)} 45%{transform:translateY(0)} 65%{transform:translateY(-5px)} 85%{transform:translateY(0)} }
            .macuin-cart-bump { animation: macuin-cart-bump 0.55s ease; }
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
    <div id="macuin-toast-host" class="fixed top-4 right-4 z-[100] flex flex-col gap-2 max-w-sm pointer-events-none" aria-live="polite"></div>
    <script>
    (function () {
        function pushToast(msg, type) {
            var host = document.getElementById('macuin-toast-host');
            if (!host || !msg) return;
            var el = document.createElement('div');
            var cls = 'bg-emerald-50 text-emerald-900 border-emerald-200';
            if (type === 'error') cls = 'bg-red-50 text-red-900 border-red-200';
            else if (type === 'info') cls = 'bg-sky-50 text-sky-900 border-sky-200';
            el.className = 'pointer-events-auto rounded-lg shadow-lg px-4 py-3 text-sm font-medium border ' + cls;
            el.textContent = msg;
            host.appendChild(el);
            setTimeout(function () { el.style.opacity = '0'; el.style.transition = 'opacity .4s'; }, 4200);
            setTimeout(function () { el.remove(); }, 4800);
        }
        window.macuinPushToast = pushToast;
        @if (session('status'))
            pushToast(@json(session('status')), 'ok');
        @endif
        @if (session('error'))
            pushToast(@json(session('error')), 'error');
        @endif
        @if (isset($errors) && $errors->any())
            @foreach ($errors->all() as $err)
                pushToast(@json($err), 'error');
            @endforeach
        @endif

        document.addEventListener('submit', function (ev) {
            var form = ev.target;
            if (!form || !form.classList || !form.classList.contains('macuin-cart-add-ajax')) return;
            ev.preventDefault();
            var token = document.querySelector('meta[name="csrf-token"]');
            if (!token) return;
            var fd = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRF-TOKEN': token.getAttribute('content'),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                },
                body: fd
            }).then(function (r) {
                return r.text().then(function (t) {
                    var j = {};
                    try { j = t ? JSON.parse(t) : {}; } catch (e) { j = {}; }
                    return { ok: r.ok, j: j };
                });
            })
            .then(function (x) {
                var msg = x.j.message;
                if (!msg && x.j.errors) {
                    var vals = Object.values(x.j.errors);
                    if (vals.length && Array.isArray(vals[0])) msg = vals[0][0];
                }
                if (!msg) msg = x.ok ? 'Listo' : 'No se pudo completar la acción.';
                pushToast(msg, x.j.ok ? 'ok' : 'error');
                if (typeof x.j.cart_count === 'number') {
                    var badge = document.getElementById('macuin-cart-badge');
                    var wrap = document.getElementById('macuin-nav-carrito');
                    if (badge) {
                        badge.textContent = x.j.cart_count > 99 ? '99+' : String(x.j.cart_count);
                        badge.classList.toggle('hidden', x.j.cart_count < 1);
                    } else if (wrap && x.j.cart_count > 0) {
                        var s = document.createElement('span');
                        s.id = 'macuin-cart-badge';
                        s.className = 'absolute -top-0.5 -right-0.5 min-w-[1.1rem] h-[1.1rem] px-1 rounded-full bg-[var(--color-macuin-yellow)] text-black text-[10px] font-bold flex items-center justify-center';
                        s.textContent = x.j.cart_count > 99 ? '99+' : String(x.j.cart_count);
                        wrap.appendChild(s);
                    }
                    if (wrap && x.j.ok) {
                        wrap.classList.remove('macuin-cart-bump');
                        void wrap.offsetWidth;
                        wrap.classList.add('macuin-cart-bump');
                        setTimeout(function () { wrap.classList.remove('macuin-cart-bump'); }, 600);
                    }
                }
            }).catch(function () {
                pushToast('No se pudo añadir al carrito. Intenta de nuevo.', 'error');
            });
        }, false);
    })();
    </script>
    @stack('scripts')
</body>
</html>
