FROM php:8.4-fpm

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libpq-dev \
    zip \
    unzip \
    libzip-dev \
    nginx \
    && docker-php-ext-install pdo_mysql pdo_pgsql mbstring exif pcntl bcmath zip opcache

# OPcache: en desarrollo (volumen ./Laravel) los timestamps deben revalidarse; si validate_timestamps=0
# PHP sigue sirviendo bytecode viejo y las vistas Blade parecen “atascadas” aunque el disco esté actualizado.
RUN docker-php-ext-enable opcache \
    && echo "opcache.enable=1" >> /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini \
    && echo "opcache.enable_cli=1" >> /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini \
    && echo "opcache.memory_consumption=256" >> /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini \
    && echo "opcache.interned_strings_buffer=16" >> /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini \
    && echo "opcache.max_accelerated_files=20000" >> /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini \
    && echo "opcache.revalidate_freq=1" >> /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini \
    && echo "opcache.validate_timestamps=1" >> /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini \
    && echo "opcache.save_comments=1" >> /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini \
    && echo "opcache.fast_shutdown=1" >> /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Leverage Docker layer caching for Composer
COPY composer.json composer.lock* ./
RUN composer install --no-dev --no-scripts --no-autoloader --prefer-dist

COPY . .

RUN composer dump-autoload --optimize

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html/storage \
    && chmod -R 755 /var/www/html/bootstrap/cache \
    && chmod -R 755 /var/www/html/bootstrap/cache || true \
    && chmod -R 755 /var/www/html/storage || true

# Create PHP-FPM pool directory and configuration
RUN mkdir -p /etc/php/8.4/fpm/pool.d
RUN echo '[www] \
listen = 0.0.0.0:9000 \
listen.backlog = 511 \
user = www-data \
group = www-data \
pm = dynamic \
pm.max_children = 50 \
pm.start_servers = 5 \
pm.min_spare_servers = 2 \
pm.max_spare_servers = 35 \
pm.max_requests = 500 \
access.log = /proc/self/fd/2 \
clear_env = no \
catch_workers_output = yes \
decorate_workers_output = no' > /etc/php/8.4/fpm/pool.d/www.conf

# Copy nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 8000

# Sin script externo: en Windows un .sh con CRLF provoca "not found" al ejecutar el shebang.
# 1. Si el named volume vacío ocultó vendor/, restaurar con composer install.
# 2. Limpiar cache stale de packages (el host bind mount puede tener refs a paquetes dev).
# 3. Ejecutar migraciones y optimizar caché (config, rutas, vistas).
# 4. Arrancar PHP-FPM en background y nginx en primer plano.
CMD ["sh", "-c", "cd /var/www/html && if [ ! -f vendor/autoload.php ]; then composer install --no-interaction --prefer-dist --optimize-autoloader 2>&1; fi; rm -f bootstrap/cache/packages.php bootstrap/cache/services.php; php artisan package:discover --ansi 2>/dev/null; php artisan migrate --force 2>/dev/null; (php artisan optimize 2>/dev/null || true); php-fpm & exec nginx -g 'daemon off;'"]
