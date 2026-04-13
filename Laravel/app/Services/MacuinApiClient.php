<?php

namespace App\Services;

use Illuminate\Http\Client\PendingRequest;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

/**
 * Wrapper centralizado para comunicación con la API FastAPI.
 *
 * - HTTP Basic Auth para escrituras (POST/PUT/PATCH/DELETE)
 * - Timeouts agresivos (connect 3s, request 5s)
 * - Retry automático (1 reintento con 150ms de delay)
 * - Cache in-memory por request para evitar llamadas duplicadas
 */
class MacuinApiClient
{
    /** @var array<string, mixed> */
    private array $requestCache = [];

    private string $baseUrl;

    private string $user;

    private string $password;

    public function __construct()
    {
        $this->baseUrl = rtrim((string) config('macuin.api_base_url', 'http://localhost:8000'), '/');
        $this->user = (string) config('macuin.api_basic_user', 'alidaniel');
        $this->password = (string) config('macuin.api_basic_password', '123456');
    }

    /**
     * GET request (read-only, no auth required by most endpoints).
     */
    public function get(string $path, array $query = [], int $cacheTtl = 0): ?array
    {
        $cacheKey = 'api_get:'.md5($path.'|'.json_encode($query));

        // In-memory per-request cache
        if (isset($this->requestCache[$cacheKey])) {
            return $this->requestCache[$cacheKey];
        }

        // Optional file/driver cache
        if ($cacheTtl > 0) {
            $cached = Cache::get($cacheKey);
            if ($cached !== null) {
                $this->requestCache[$cacheKey] = $cached;

                return $cached;
            }
        }

        try {
            $response = $this->readClient()
                ->get($this->baseUrl.$path, $query);

            $data = $this->parseResponse($response);

            $this->requestCache[$cacheKey] = $data;

            if ($cacheTtl > 0 && $data !== null) {
                Cache::put($cacheKey, $data, $cacheTtl);
            }

            return $data;
        } catch (\Throwable $e) {
            Log::warning("MacuinApiClient GET {$path} failed: {$e->getMessage()}");

            return null;
        }
    }

    /**
     * GET with authentication (for protected read endpoints).
     */
    public function getAuth(string $path, array $query = []): ?array
    {
        try {
            $response = $this->writeClient()
                ->get($this->baseUrl.$path, $query);

            return $this->parseResponse($response);
        } catch (\Throwable $e) {
            Log::warning("MacuinApiClient GET(auth) {$path} failed: {$e->getMessage()}");

            return null;
        }
    }

    /**
     * POST request (with auth).
     *
     * @return array{ok: bool, data: ?array, status: int}
     */
    public function post(string $path, array $body = []): array
    {
        try {
            $response = $this->writeClient()
                ->post($this->baseUrl.$path, $body);

            return [
                'ok' => $response->successful(),
                'data' => $this->parseResponse($response),
                'status' => $response->status(),
            ];
        } catch (\Throwable $e) {
            Log::warning("MacuinApiClient POST {$path} failed: {$e->getMessage()}");

            return ['ok' => false, 'data' => null, 'status' => 500];
        }
    }

    /**
     * PATCH request (with auth).
     *
     * @return array{ok: bool, data: ?array, status: int}
     */
    public function patch(string $path, array $body = []): array
    {
        try {
            $response = $this->writeClient()
                ->patch($this->baseUrl.$path, $body);

            return [
                'ok' => $response->successful(),
                'data' => $this->parseResponse($response),
                'status' => $response->status(),
            ];
        } catch (\Throwable $e) {
            Log::warning("MacuinApiClient PATCH {$path} failed: {$e->getMessage()}");

            return ['ok' => false, 'data' => null, 'status' => 500];
        }
    }

    /**
     * PUT request (with auth).
     *
     * @return array{ok: bool, data: ?array, status: int}
     */
    public function put(string $path, array $body = []): array
    {
        try {
            $response = $this->writeClient()
                ->put($this->baseUrl.$path, $body);

            return [
                'ok' => $response->successful(),
                'data' => $this->parseResponse($response),
                'status' => $response->status(),
            ];
        } catch (\Throwable $e) {
            Log::warning("MacuinApiClient PUT {$path} failed: {$e->getMessage()}");

            return ['ok' => false, 'data' => null, 'status' => 500];
        }
    }

    /**
     * DELETE request (with auth).
     *
     * @return array{ok: bool, status: int}
     */
    public function delete(string $path): array
    {
        try {
            $response = $this->writeClient()
                ->delete($this->baseUrl.$path);

            return [
                'ok' => $response->successful(),
                'status' => $response->status(),
            ];
        } catch (\Throwable $e) {
            Log::warning("MacuinApiClient DELETE {$path} failed: {$e->getMessage()}");

            return ['ok' => false, 'status' => 500];
        }
    }

    /**
     * Flush in-memory cache (useful in long-running processes).
     */
    public function flushRequestCache(): void
    {
        $this->requestCache = [];
    }

    // ─── Internals ────────────────────────────────────────

    private function readClient(): PendingRequest
    {
        return Http::connectTimeout(3)
            ->timeout(5)
            ->retry(1, 150, throw: false)
            ->acceptJson();
    }

    private function writeClient(): PendingRequest
    {
        return Http::connectTimeout(3)
            ->timeout(5)
            ->retry(1, 150, throw: false)
            ->withBasicAuth($this->user, $this->password)
            ->acceptJson();
    }

    private function parseResponse(Response $response): ?array
    {
        if (! $response->successful()) {
            return null;
        }

        $body = $response->body();
        if ($body === '' || $body === 'null') {
            return null;
        }

        $json = $response->json();

        return is_array($json) ? $json : null;
    }
}
