<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Http;

/*
|--------------------------------------------------------------------------
| MACUIN - Rutas web
|--------------------------------------------------------------------------
*/

// Página de selección de tipo de usuario (entrada principal)
Route::get('/', function () {
    return view('selector');
})->name('selector');

// Acceso Personal - Redirige a través de la API siguiendo las mejores prácticas
Route::get('/personal/ingresar', function () {
    try {
        $apiBaseUrl = env('API_BASE_URL', 'http://localhost:8000');
        $response = Http::get("{$apiBaseUrl}/v1/redirect/personal");
        
        if ($response->successful()) {
            $data = $response->json();
            return redirect()->away($data['url']);
        }
        
        // Fallback o manejo de error si la API no responde
        return redirect()->away(env('FLASK_URL', 'http://localhost:5000') . '/login');
        
    } catch (\Exception $e) {
        // En caso de error crítico, usar valor por defecto configurado
        return redirect()->away(env('FLASK_URL', 'http://localhost:5000') . '/login');
    }
})->name('personal.login');

// Área clientes - Páginas principales
Route::get('/inicio', function () {
    return view('home');
})->name('inicio');

Route::get('/ingresar', function () {
    return view('auth.login');
})->name('login');

Route::get('/registro', function () {
    return view('auth.register');
})->name('registro');

Route::get('/catalogo', function () {
    return view('catalogo');
})->name('catalogo');

Route::get('/pedidos', function () {
    return view('pedidos');
})->name('pedidos');

Route::get('/contacto', function () {
    return view('contacto');
})->name('contacto');

Route::get('/carrito', function () {
    return view('carrito');
})->name('carrito');

Route::get('/pago', function () {
    return view('pago');
})->name('pago');
