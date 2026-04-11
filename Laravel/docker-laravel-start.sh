#!/bin/sh
# Limpia cachés de Laravel al arrancar el contenedor (vistas Blade, rutas, config) para que
# los cambios en el host se reflejen sin tener que entrar manualmente al contenedor.
cd /var/www/html || exit 1
if [ -f artisan ]; then
    php artisan optimize:clear >/dev/null 2>&1 || true
fi
php-fpm &
exec nginx -g 'daemon off;'
