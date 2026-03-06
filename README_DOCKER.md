# Dockerización del Proyecto Macuin

## Arquitectura de Servicios

El proyecto contiene los siguientes servicios dockerizados:

- **API FastAPI**: Puerto 8000
- **Aplicación Flask**: Puerto 5000  
- **Aplicación Laravel**: Puerto 9000

## Instrucciones de Uso

### 1. Construir y levantar todos los servicios
```bash
docker-compose up --build -d
```

### 2. Verificar el estado de los contenedores
```bash
docker-compose ps
```

### 3. Ver logs de un servicio específico
```bash
# API FastAPI
docker-compose logs -f api

# Flask
docker-compose logs -f flask

# Laravel
docker-compose logs -f laravel
```

### 4. Detener todos los servicios
```bash
docker-compose down
```

### 5. Reconstruir un servicio específico
```bash
docker-compose up --build -d api
```

## Configuración de Puertos

| Servicio | Puerto Host | Puerto Contenedor |
|----------|-------------|-------------------|
| API FastAPI | 8000 | 8000 |
| Flask | 5000 | 5000 |
| Laravel (PHP-FPM) | 9000 | 9000 |

## Consideraciones Adicionales

1. Los archivos `.env` locales son ignorados por Docker (ver archivos `.dockerignore`)
2. Todos los servicios están conectados a una red interna `macuin_network`
3. Los templates de Laravel tienen permisos configurados correctamente

