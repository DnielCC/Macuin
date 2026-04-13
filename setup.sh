#!/bin/bash

set -e

# ── Colores ──────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ── Funciones de utilidad ────────────────────────────────────
info()    { echo -e "${CYAN}ℹ  $1${NC}"; }
success() { echo -e "${GREEN}✔  $1${NC}"; }
warn()    { echo -e "${YELLOW}⚠  $1${NC}"; }
error()   { echo -e "${RED}✖  $1${NC}"; }
header()  { echo -e "\n${BOLD}${CYAN}═══ $1 ═══${NC}\n"; }

# ── Docker Compose command ───────────────────────────────────
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# ═══════════════════════════════════════════════════════════════
#  Función: verificar prerequisitos
# ═══════════════════════════════════════════════════════════════
verificar_prerequisitos() {
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

    if ! docker info &> /dev/null; then
        error "Docker no está corriendo. Inicia Docker Desktop y vuelve a intentar."
        exit 1
    fi
    success "Docker está corriendo"
}

# ═══════════════════════════════════════════════════════════════
#  Función: configurar .env de Laravel (solo primera vez)
# ═══════════════════════════════════════════════════════════════
configurar_env() {
    header "Configurando archivos de entorno"

    if [ ! -f "./Laravel/.env" ]; then
        cp ./Laravel/.env.example ./Laravel/.env

        # Configurar SESSION y CACHE como 'file' (evita SQLite sobre volumen Docker)
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
}

# ═══════════════════════════════════════════════════════════════
#  Función: construir y levantar contenedores
#  $1 = "build" para --build, vacío para solo levantar
# ═══════════════════════════════════════════════════════════════
levantar_contenedores() {
    local BUILD_FLAG="$1"

    if [ "$BUILD_FLAG" = "build" ]; then
        header "Construyendo y levantando contenedores Docker"
        info "Esto puede tardar unos minutos la primera vez..."
        $COMPOSE_CMD up --build -d
    else
        header "Levantando contenedores Docker"
        $COMPOSE_CMD up -d
    fi

    success "Contenedores levantados correctamente"
}

# ═══════════════════════════════════════════════════════════════
#  Función: esperar a que PostgreSQL esté listo
# ═══════════════════════════════════════════════════════════════
esperar_postgres() {
    header "Esperando a que PostgreSQL esté listo"

    local MAX_RETRIES=30
    local RETRY_COUNT=0

    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if docker exec macuin_db pg_isready -U macuin -d DB_macuin &> /dev/null; then
            success "PostgreSQL está listo y aceptando conexiones"
            return 0
        fi
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo -ne "  Esperando... ($RETRY_COUNT/$MAX_RETRIES)\r"
        sleep 2
    done

    error "PostgreSQL no respondió a tiempo. Revisa los logs con: $COMPOSE_CMD logs postgres"
    exit 1
}

# ═══════════════════════════════════════════════════════════════
#  Función: esperar a que la API FastAPI esté lista
# ═══════════════════════════════════════════════════════════════
esperar_api() {
    header "Verificando API FastAPI"

    local MAX_RETRIES=20
    local RETRY_COUNT=0

    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs 2>/dev/null | grep -q "200"; then
            success "API FastAPI respondiendo en http://localhost:8000"
            return 0
        fi
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo -ne "  Esperando API... ($RETRY_COUNT/$MAX_RETRIES)\r"
        sleep 2
    done

    warn "La API aún no responde. Puede necesitar más tiempo."
    info "Revisa los logs con: $COMPOSE_CMD logs api"
}

# ═══════════════════════════════════════════════════════════════
#  Función: configurar Laravel (composer, key, permisos, migrate)
# ═══════════════════════════════════════════════════════════════
configurar_laravel() {
    header "Configurando Laravel"

    if [ ! -d "./Laravel/vendor" ]; then
        info "Instalando dependencias de Composer (primera vez)..."
        docker exec macuin_laravel composer install --no-interaction --prefer-dist --optimize-autoloader 2>/dev/null
        success "Dependencias de Composer instaladas"
    else
        info "Verificando dependencias de Composer..."
        docker exec macuin_laravel composer install --no-interaction --prefer-dist --optimize-autoloader 2>/dev/null
        success "Dependencias de Composer revisadas"
    fi

    if ! grep -q "APP_KEY=base64:" ./Laravel/.env; then
        info "Generando Application Key..."
        docker exec macuin_laravel php artisan key:generate --force 2>/dev/null
        success "Application Key generada"
    fi

    info "Configurando permisos de storage y cache..."
    docker exec macuin_laravel sh -c 'chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache' 2>/dev/null || true
    docker exec macuin_laravel sh -c 'chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache' 2>/dev/null || true
    success "Permisos configurados"

    info "Sincronizando Base de Datos de Laravel (SQLite)..."
    if [ ! -f "./Laravel/database/database.sqlite" ]; then
        touch ./Laravel/database/database.sqlite
    fi
    docker exec macuin_laravel php artisan migrate --force 2>/dev/null
    success "Tablas de Laravel sincronizadas"

    info "Optimizando caché de Laravel (config, rutas, vistas)..."
    docker exec macuin_laravel php artisan optimize 2>/dev/null || true
    success "Laravel optimizado"
}

# ═══════════════════════════════════════════════════════════════
#  Función: inicializar BD PostgreSQL (tablas + datos de prueba)
#
#  Orden obligatorio:
#    1. init_db.py       → Crea tablas + seed_fase1 (roles, estatus, usuario sistema)
#    2. seed_full_data.py → Categorías, marcas, autopartes, ubicaciones, inventarios
#    3. seed_macuin_demo_users.py → Usuarios demo para login Flask
# ═══════════════════════════════════════════════════════════════
inicializar_postgres() {
    header "Inicializando PostgreSQL (tablas y datos de prueba)"

    # PASO 1: Crear tablas + seed mínimo (roles, estatus, usuario sistema)
    info "Paso 1/3: Creando tablas y seed base (roles, estatus, usuario sistema)..."
    if docker exec macuin_api python scripts/init_db.py 2>&1; then
        success "Tablas y seed base aplicados correctamente"
    else
        error "Error al crear tablas. Revisa los logs: $COMPOSE_CMD logs api"
        exit 1
    fi

    # PASO 2: Seed de datos completos (categorías, marcas, autopartes, inventarios)
    info "Paso 2/3: Cargando datos de catálogo (categorías, marcas, autopartes, inventarios)..."
    if docker exec macuin_api python scripts/seed_full_data.py 2>&1; then
        success "Datos de catálogo cargados"
    else
        warn "No se pudieron cargar datos de catálogo (pueden ya existir)"
    fi

    # PASO 3: Usuarios demo para Flask
    info "Paso 3/3: Creando usuarios demo para login Flask..."
    if docker exec macuin_api python scripts/seed_macuin_demo_users.py 2>&1; then
        success "Usuarios demo creados/actualizados"
    else
        warn "No se pudieron crear usuarios demo"
    fi
}

# ═══════════════════════════════════════════════════════════════
#  Función: verificar Flask
# ═══════════════════════════════════════════════════════════════
esperar_flask() {
    header "Verificando Flask"

    local MAX_RETRIES=15
    local RETRY_COUNT=0

    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/ 2>/dev/null | grep -qE "200|302"; then
            success "Flask respondiendo en http://localhost:5001"
            return 0
        fi
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo -ne "  Esperando Flask... ($RETRY_COUNT/$MAX_RETRIES)\r"
        sleep 2
    done

    warn "Flask aún no responde. Puede necesitar más tiempo."
    info "Revisa los logs con: $COMPOSE_CMD logs flask"
}

# ═══════════════════════════════════════════════════════════════
#  Función: resumen final
# ═══════════════════════════════════════════════════════════════
resumen_final() {
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
    echo -e "  ${CYAN}Reconstruir:${NC}      bash setup.sh rebuild"
    echo -e "  ${CYAN}Inicio rápido:${NC}    bash setup.sh start"
    echo -e "  ${CYAN}Estado:${NC}           $COMPOSE_CMD ps"
    echo ""
    echo -e "${BOLD}Credenciales demo Flask:${NC}"
    echo ""
    echo -e "  ${CYAN}Admin:${NC}      admin@macuin.com     / admin123"
    echo -e "  ${CYAN}Ventas:${NC}     ventas@macuin.com    / ventas123"
    echo -e "  ${CYAN}Logística:${NC}  logistica@macuin.com / logistica123"
    echo -e "  ${CYAN}Almacén:${NC}    almacen@macuin.com   / almacen123"
    echo ""
}

# ═══════════════════════════════════════════════════════════════
#  Auto-detectar modo si no se pasa argumento
# ═══════════════════════════════════════════════════════════════
detectar_modo() {
    # Si los contenedores no existen → build (primera vez)
    if ! docker ps -a --format '{{.Names}}' | grep -q "macuin_db"; then
        echo "build"
        return
    fi

    # Si los contenedores existen pero están parados → start
    if ! docker ps --format '{{.Names}}' | grep -q "macuin_db"; then
        echo "start"
        return
    fi

    # Si ya están corriendo → start (solo verificar BD)
    echo "start"
}

# ═══════════════════════════════════════════════════════════════
#  MAIN — Ejecutar según modo
# ═══════════════════════════════════════════════════════════════

MODE="${1:-$(detectar_modo)}"

case "$MODE" in

    # ─────────────────────────────────────────────────────────
    #  MODO 1: build — Primera vez (todo desde cero)
    # ─────────────────────────────────────────────────────────
    build)
        header "🔨 MODO: Primera vez — Construyendo todo desde cero"

        verificar_prerequisitos
        configurar_env
        levantar_contenedores "build"
        esperar_postgres
        esperar_api
        configurar_laravel
        inicializar_postgres
        esperar_flask
        resumen_final
        ;;

    # ─────────────────────────────────────────────────────────
    #  MODO 2: rebuild — Reconstruir contenedores (cambios de código)
    # ─────────────────────────────────────────────────────────
    rebuild)
        header "🔄 MODO: Reconstruir contenedores con cambios"

        verificar_prerequisitos
        levantar_contenedores "build"
        esperar_postgres
        esperar_api
        configurar_laravel
        inicializar_postgres
        esperar_flask
        resumen_final
        ;;

    # ─────────────────────────────────────────────────────────
    #  MODO 3: start — Inicio rápido (solo levantar + verificar BD)
    # ─────────────────────────────────────────────────────────
    start)
        header "🚀 MODO: Inicio rápido — Levantando y verificando BD"

        verificar_prerequisitos
        levantar_contenedores ""
        esperar_postgres
        esperar_api
        inicializar_postgres
        esperar_flask
        resumen_final
        ;;

    # ─────────────────────────────────────────────────────────
    #  Ayuda
    # ─────────────────────────────────────────────────────────
    help|--help|-h)
        echo ""
        echo -e "${BOLD}MACUIN — Setup Script${NC}"
        echo ""
        echo -e "  ${CYAN}bash setup.sh${NC}           Auto-detecta el modo necesario"
        echo -e "  ${CYAN}bash setup.sh build${NC}     Primera vez: construye todo desde cero"
        echo -e "  ${CYAN}bash setup.sh rebuild${NC}   Reconstruir contenedores (cambios de código)"
        echo -e "  ${CYAN}bash setup.sh start${NC}     Inicio rápido: levantar + verificar BD"
        echo ""
        ;;

    *)
        error "Modo desconocido: '$MODE'"
        echo -e "  Usa: ${CYAN}bash setup.sh [build|rebuild|start|help]${NC}"
        exit 1
        ;;
esac