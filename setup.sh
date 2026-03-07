#!/bin/bash

echo "Levantando contenedores de Docker..."
docker-compose up -d

echo "Esperando 5 segundos para que Laravel inicie..."
sleep 3

echo "Instalando dependencias de Composer..."
docker exec -it macuin_laravel composer install

echo "Configurando archivo .env..."
if [ ! -f "./Laravel/.env" ]; then
    cp ./Laravel/.env.example ./Laravel/.env
    # Cambiamos a 'file' para evitar el error de SQLite
    sed -i 's/SESSION_DRIVER=database/SESSION_DRIVER=file/g' ./Laravel/.env
    sed -i 's/CACHE_STORE=database/CACHE_STORE=file/g' ./Laravel/.env
    echo "Archivo .env creado y configurado."
else
    echo "El archivo .env ya existe. Omitiendo..."
fi

echo "Generando Application Key..."
docker exec -it macuin_laravel php artisan key:generate

echo "Restaurando permisos de carpetas..."
docker exec -it macuin_laravel chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache
docker exec -it macuin_laravel chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

echo "Limpiando cache..."
docker exec -it macuin_laravel php artisan optimize:clear

echo "Ingresa a http://localhost:8002/"