#!/bin/bash

#  Uso:  bash setup.sh

set -e  # Detener al primer error

# ── Colores ──────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # Sin color

# ── Funciones de utilidad ────────────────────────────────────
info()    { echo -e "${CYAN}ℹ  $1${NC}"; }
success() { echo -e "${GREEN}✔  $1${NC}"; }
warn()    { echo -e "${YELLOW}⚠  $1${NC}"; }
error()   { echo -e "${RED}✖  $1${NC}"; }
header()  { echo -e "\n${BOLD}${CYAN}═══ $1 ═══${NC}\n"; }

# ── 1. Verificar prerequisitos ───────────────────────────────
header "Verificando prerequisitos"

if ! command -v docker &> /dev/null; then
    error "Docker no está instalado. Instálalo desde https://docs.docker.com/get-docker/"
    exit 1
fi
success "Docker encontrado: $(docker --version)"

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    error "Docker Compose no está instalado."
    exit 1
fi
success "Docker Compose encontrado"

# Verificar que Docker está corriendo
if ! docker info &> /dev/null; then
    error "Docker no está corriendo. Inicia Docker Desktop y vuelve a intentar."
    exit 1
fi
success "Docker está corriendo"

# ── 2. Configurar archivo .env de Laravel ────────────────────
header "Configurando archivos de entorno"

if [ ! -f "./Laravel/.env" ]; then
    cp ./Laravel/.env.example ./Laravel/.env

    # Configurar SESSION y CACHE como 'file' para evitar errores de SQLite
    sed -i 's/SESSION_DRIVER=database/SESSION_DRIVER=file/g' ./Laravel/.env
    sed -i 's/CACHE_STORE=database/CACHE_STORE=file/g' ./Laravel/.env

    # Agregar URLs de servicios internos
    if ! grep -q "API_BASE_URL" ./Laravel/.env; then
        echo "" >> ./Laravel/.env
        echo "# Configuración de servicios externos" >> ./Laravel/.env
        echo "API_BASE_URL=http://macuin_api:8000" >> ./Laravel/.env
        echo "FLASK_URL=http://macuin_flask:5001" >> ./Laravel/.env
    fi

    success "Archivo Laravel/.env creado y configurado"
else
    warn "Laravel/.env ya existe. Se omite la creación."
fi

# ── 3. Construir y levantar contenedores ─────────────────────
header "Construyendo y levantando contenedores Docker"

info "Esto puede tardar unos minutos la primera vez..."

# Usar 'docker compose' (V2) o 'docker-compose' (V1)
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

$COMPOSE_CMD up --build -d

success "Contenedores levantados correctamente"

# ── 4. Esperar a que PostgreSQL esté listo ───────────────────
header "Esperando a que PostgreSQL esté listo"

MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if docker exec macuin_db pg_isready -U macuin -d DB_macuin &> /dev/null; then
        success "PostgreSQL está listo y aceptando conexiones"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -ne "  Esperando... ($RETRY_COUNT/$MAX_RETRIES)\r"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    error "PostgreSQL no respondió a tiempo. Revisa los logs con: $COMPOSE_CMD logs postgres"
    exit 1
fi

# ── 5. Verificar API FastAPI ─────────────────────────────────
header "Verificando API FastAPI"

MAX_RETRIES=20
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs 2>/dev/null | grep -q "200"; then
        success "API FastAPI respondiendo en http://localhost:8000"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -ne "  Esperando API... ($RETRY_COUNT/$MAX_RETRIES)\r"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    warn "La API aún no responde. Puede necesitar más tiempo."
    info "Revisa los logs con: $COMPOSE_CMD logs api"
fi

# ── 6. Configurar Laravel dentro del contenedor ─────────────
header "Configurando Laravel"

info "Instalando dependencias de Composer..."
docker exec macuin_laravel composer install --no-interaction --prefer-dist --optimize-autoloader 2>/dev/null
success "Dependencias de Composer instaladas"

info "Generando Application Key..."
docker exec macuin_laravel php artisan key:generate --force 2>/dev/null
success "Application Key generada"

info "Configurando permisos de storage y cache..."
docker exec macuin_laravel chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache
docker exec macuin_laravel chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache
success "Permisos configurados"

info "Limpiando caché de Laravel..."
docker exec macuin_laravel php artisan optimize:clear 2>/dev/null
success "Caché limpiada"

# ── 7. Crear tablas en PostgreSQL (API) ──────────────────────
header "Inicializando base de datos"

info "Creando tablas y seed FASE 1 (SQLAlchemy + scripts/init_db.py)..."
docker exec macuin_api python scripts/init_db.py 2>/dev/null && success "Base de datos inicializada (tablas + seed si aplica)" || warn "No se pudo inicializar la BD. Revisa: docker compose logs api"

# ── 8. Verificar que Flask está corriendo ────────────────────
header "Verificando Flask"

MAX_RETRIES=15
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/ 2>/dev/null | grep -qE "200|302"; then
        success "Flask respondiendo en http://localhost:5001"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -ne "  Esperando Flask... ($RETRY_COUNT/$MAX_RETRIES)\r"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    warn "Flask aún no responde. Puede necesitar más tiempo."
    info "Revisa los logs con: $COMPOSE_CMD logs flask"
fi

# ── 9. Resumen final ────────────────────────────────────────
header "🎉 ¡Setup completado!"

echo -e "${BOLD}Servicios disponibles:${NC}"
echo ""
echo -e "  ${GREEN}📦 PostgreSQL${NC}     → localhost:${BOLD}5433${NC}  (Uso exclusivo de la API)"
echo -e "  ${GREEN}⚡ API FastAPI${NC}    → http://localhost:${BOLD}8000${NC}"
echo -e "  ${GREEN}📖 API Docs${NC}       → http://localhost:${BOLD}8000/docs${NC}"
echo -e "  ${GREEN}🌐 Flask (Front)${NC}  → http://localhost:${BOLD}5001${NC}"
echo -e "  ${GREEN}🔷 Laravel${NC}        → http://localhost:${BOLD}8003${NC}"
echo ""
echo -e "${BOLD}Comandos útiles:${NC}"
echo ""
echo -e "  ${CYAN}Ver logs:${NC}         $COMPOSE_CMD logs -f [api|flask|laravel|postgres]"
echo -e "  ${CYAN}Detener todo:${NC}     $COMPOSE_CMD down"
echo -e "  ${CYAN}Reconstruir:${NC}      $COMPOSE_CMD up --build -d"
echo -e "  ${CYAN}Estado:${NC}           $COMPOSE_CMD ps"
echo ""