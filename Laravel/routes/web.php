<?php

use App\Http\Controllers\AccountController;
use App\Http\Controllers\Auth\AuthenticatedSessionController;
use App\Http\Controllers\Auth\RegisteredUserController;
use App\Http\Controllers\CartController;
use App\Http\Controllers\CatalogController;
use App\Http\Controllers\CheckoutController;
use App\Http\Controllers\ContactController;
use App\Http\Controllers\ContactInboxController;
use App\Http\Controllers\HomeController;
use App\Http\Controllers\PedidosController;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('selector');
})->name('selector');

Route::get('/personal/ingresar', function () {
    try {
        $apiBaseUrl = config('macuin.api_base_url', 'http://localhost:8000');
        $response = Http::timeout(8)->get("{$apiBaseUrl}/v1/redirect/personal");

        if ($response->successful()) {
            $data = $response->json();

            return redirect()->away($data['url']);
        }

        $flaskUrl = config('macuin.flask_url', 'http://localhost:5000');
        return redirect()->away($flaskUrl.'/login');
    } catch (\Exception $e) {
        $flaskUrl = config('macuin.flask_url', 'http://localhost:5000');
        return redirect()->away($flaskUrl.'/login');
    }
})->name('personal.login');

Route::get('/inicio', [HomeController::class, 'index'])->name('inicio');

Route::middleware('guest')->group(function () {
    Route::get('/ingresar', [AuthenticatedSessionController::class, 'create'])->name('login');
    Route::post('/ingresar', [AuthenticatedSessionController::class, 'store'])
        ->middleware('throttle:12,1')
        ->name('login.store');

    Route::get('/registro', [RegisteredUserController::class, 'create'])->name('registro');
    Route::post('/registro', [RegisteredUserController::class, 'store'])
        ->middleware('throttle:8,1')
        ->name('registro.store');
});

Route::middleware('auth')->group(function () {
    Route::get('/mi-cuenta', [AccountController::class, 'show'])->name('cuenta');
    Route::post('/salir', [AuthenticatedSessionController::class, 'destroy'])->name('logout');
});

Route::get('/catalogo', [CatalogController::class, 'index'])->name('catalogo');

Route::middleware(['auth', 'throttle:40,1'])->group(function () {
    Route::get('/carrito', [CartController::class, 'index'])->name('carrito');
    Route::post('/carrito/agregar', [CartController::class, 'add'])->name('carrito.agregar');
    Route::post('/carrito/linea/{linea}/quitar', [CartController::class, 'remove'])->name('carrito.quitar');
    Route::post('/carrito/linea/{linea}/cantidad', [CartController::class, 'updateQty'])->name('carrito.cantidad');

    Route::get('/pago', [CheckoutController::class, 'show'])->name('pago');
    Route::post('/pago/procesar', [CheckoutController::class, 'procesar'])
        ->middleware('throttle:10,1')
        ->name('pago.procesar');

    Route::get('/pedidos', [PedidosController::class, 'index'])->name('pedidos');
    Route::post('/pedidos/{pedido}/cancelar', [PedidosController::class, 'cancelar'])
        ->middleware('throttle:10,1')
        ->name('pedidos.cancelar');
});

Route::get('/contacto', [ContactController::class, 'create'])->name('contacto');
Route::post('/contacto', [ContactController::class, 'store'])
    ->middleware('throttle:8,1')
    ->name('contacto.store');

Route::middleware(['auth', 'macuin.admin.contact', 'throttle:60,1'])->prefix('admin-portal')->group(function () {
    Route::get('/mensajes-contacto', [ContactInboxController::class, 'index'])->name('admin.contacto.inbox');
    Route::post('/mensajes-contacto/{mensaje}/leido', [ContactInboxController::class, 'marcarLeido'])
        ->name('admin.contacto.leido');
    Route::post('/mensajes-contacto/{mensaje}/responder', [ContactInboxController::class, 'responder'])
        ->name('admin.contacto.responder');
});
