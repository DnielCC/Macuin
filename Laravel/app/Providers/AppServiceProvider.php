<?php

namespace App\Providers;

use App\Services\PortalCartService;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\Facades\View;
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

        View::composer('layouts.partials.header', function ($view) {
            $n = 0;
            $showInbox = false;
            if (auth()->check()) {
                try {
                    $n = app(PortalCartService::class)->lineCount((int) auth()->id());
                } catch (\Throwable $e) {
                    report($e);
                }
                $allowed = config('macuin.admin_contact_emails', []);
                $em = strtolower(trim((string) auth()->user()->email));
                $showInbox = $allowed !== [] && in_array($em, $allowed, true);
            }
            $view->with('macuinCarritoCount', $n);
            $view->with('macuinShowContactInbox', $showInbox);
        });
    }
}
