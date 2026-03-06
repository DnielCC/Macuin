<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| MACUIN - Rutas web
|--------------------------------------------------------------------------
*/

// Página de selección de tipo de usuario (entrada principal)
Route::get('/', function () {
    return view('selector');
})->name('selector');

// Acceso Personal (placeholder: misma vista selector o futura vista login personal)
Route::get('/personal/ingresar', function () {
    return view('selector'); // TODO: vista login personal interno
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
