# Dockerización del Proyecto Macuin

## Requisitos Previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- [Git](https://git-scm.com/) instalado
- Puerto **5433**, **8000**, **5001** y **8003** disponibles

## Setup Rápido (Una sola línea)

```bash
bash setup.sh
```

> El script se encarga de todo: verificar Docker, construir imágenes, crear tablas en la base de datos, configurar Laravel, y verificar que todos los servicios estén arrancando correctamente.

## Arquitectura de Servicios

```
┌─────────────────────────────────────────────────────┐
│                   macuin_network                    │
│                                                     │
│        ┌──────────────┐      ┌──────────────┐       │
│        │    Flask     │      │   Laravel    │       │
│        │    :5001     │      │    :8003     │       │
│        └──────┬───────┘      └──────┬───────┘       │
│               │                     │               │
│               └──────────┬──────────┘               │
│                          ▼                          │
│                  ┌──────────────┐                   │
│                  │  API FastAPI │                   │
│                  │    :8000     │                   │
│                  └──────┬───────┘                   │
│                         │                           │
│                         ▼                           │
│                  ┌──────────────┐                   │
│                  │  PostgreSQL  │                   │
│                  │    :5433     │                   │
│                  └──────────────┘                   │
└─────────────────────────────────────────────────────┘
```

## Servicios y Puertos

| Servicio           | Contenedor       | Puerto Host | Puerto Contenedor | Descripción                     |
|--------------------|------------------|-------------|-------------------|---------------------------------|
| **PostgreSQL 15**  | `macuin_db`      | 5433        | 5432              | Base de datos principal         |
| **FastAPI**        | `macuin_api`     | 8000        | 8000              | API REST (backend)              |
| **Flask**          | `macuin_flask`   | 5001        | 5001              | Aplicación web (frontend)       |
| **Laravel + Nginx**| `macuin_laravel` | 8003        | 8000              | Panel de administración         |

## URLs de Acceso

| Servicio              | URL                              |
|-----------------------|----------------------------------|
| API FastAPI           | http://localhost:8000             |
| Documentación API     | http://localhost:8000/docs        |
| App Flask             | http://localhost:5001             |
| Laravel               | http://localhost:8003             |

## Credenciales de Base de Datos (Solo para la API)

| Campo     | Valor      |
|-----------|------------|
| Host      | `localhost` (externo) / `postgres` (interno para la API) |
| Puerto    | `5433`     |
| Base      | `DB_macuin`|
| Usuario   | `macuin`   |
| Contraseña| `123456`   |

## Comandos Útiles

### Levantar servicios
```bash
# Levantar todo (construir si es necesario)
docker compose up --build -d

# Levantar un servicio específico
docker compose up --build -d api
```

### Ver logs
```bash
# Todos los servicios
docker compose logs -f

# Servicio específico
docker compose logs -f api
docker compose logs -f flask
docker compose logs -f laravel
docker compose logs -f postgres
```

### Gestión de contenedores
```bash
# Ver estado de los contenedores
docker compose ps

# Detener todos los servicios
docker compose down

# Detener y borrar volúmenes (⚠️ OJO: borra la base de datos)
docker compose down -v

# Reiniciar un servicio
docker compose restart api
```

### Acceder a un contenedor
```bash
# Entrar a la base de datos
docker exec -it macuin_db psql -U macuin -d DB_macuin

# Entrar al contenedor de la API
docker exec -it macuin_api bash

# Entrar al contenedor de Laravel
docker exec -it macuin_laravel bash
```

## Solución de Problemas

### La API no responde
```bash
docker compose logs api
# Verificar que PostgreSQL esté corriendo:
docker exec macuin_db pg_isready -U macuin -d DB_macuin
```

### Laravel muestra error 500
```bash
docker exec macuin_laravel php artisan optimize:clear
docker exec macuin_laravel chown -R www-data:www-data /var/www/html/storage
```

### Puerto en uso
Si un puerto ya está ocupado, edita `docker-compose.yml` y cambia el puerto en la sección `ports` del servicio correspondiente.

### Reconstruir desde cero
```bash
docker compose down -v
docker compose up --build -d
bash setup.sh
```

## Consideraciones

1. Los archivos `.env` locales son ignorados por Docker (ver `.dockerignore`)
2. Todos los servicios están conectados a la red interna `macuin_network`
3. Los volúmenes de código están montados para desarrollo (hot-reload)
4. PostgreSQL usa un volumen persistente (`postgres_data`)
