FROM php:8.2-fpm

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    libzip-dev \
    nginx \
    && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath zip

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

COPY . .

RUN composer install --no-dev --optimize-autoloader

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html/storage \
    && chmod -R 755 /var/www/html/bootstrap/cache \
    && chmod -R 755 /var/www/html/resources/views

# Create PHP-FPM pool directory and configuration
RUN mkdir -p /etc/php/8.2/fpm/pool.d
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
decorate_workers_output = no' > /etc/php/8.2/fpm/pool.d/www.conf

# Copy nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 8000

# Start nginx and php-fpm
CMD ["sh", "-c", "php-fpm & nginx -g 'daemon off;'"]
