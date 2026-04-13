<?php

namespace App\Providers;

use App\Services\PortalCartService;
use Illuminate\Support\Facades\Cache;
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
                    $userId = (int) auth()->id();
                    $n = Cache::remember("cart_count_{$userId}", 30, function () use ($userId) {
                        return app(PortalCartService::class)->lineCount($userId);
                    });
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
