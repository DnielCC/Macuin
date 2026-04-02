<?php

namespace App\Providers;

use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // Las URLs absolutas de route() deben usar el mismo host y puerto que el navegador
        // (p. ej. http://localhost:8003 con Docker), no solo APP_URL sin puerto.
        if (! $this->app->runningInConsole() && request()) {
            URL::forceRootUrl(request()->getSchemeAndHttpHost());
        }
    }
}
