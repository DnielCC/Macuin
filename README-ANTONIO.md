# Macuin — Guía de trabajo (README-ANTONIO)

Este documento concentra el plan por fases del proyecto Macuin, la ubicación del **modelo de datos** que define las tablas de la FASE 1 (PostgreSQL vía API FastAPI / SQLAlchemy) y el detalle de cada fase hasta una entrega completa.

---

## Dónde ver las tablas que crearemos en la FASE 1

Las tablas de negocio **no** están en un único archivo SQL en el repositorio: están definidas como **modelos SQLAlchemy** en Python, cada uno con `__tablename__` (nombre real de la tabla en PostgreSQL).

### Carpeta principal (ábrela en el editor)

Ruta del proyecto:

`Macuin/API/database/`

Desde Cursor: **Ctrl+P** (o **Cmd+P** en macOS), escribe `API/database/` y elige el archivo que quieras revisar.

### Archivo índice (importa todos los modelos)

| Archivo | Para qué sirve |
|--------|----------------|
| `API/database/__init__.py` | Importa todas las clases modelo. Cuando se ejecuta `Base.metadata.create_all(bind=engine)`, SQLAlchemy recorre estos modelos y **crea las tablas** que aún no existan. |

### Archivo de conexión al motor

| Archivo | Para qué sirve |
|--------|----------------|
| `API/database/db.py` | URL de base de datos (`DATABASE_URL`), motor `create_engine`, `SessionLocal` y `Base`. Es el “cable” hacia PostgreSQL, no define tablas por sí solo. |

### Tabla ↔ archivo (definición de columnas y relaciones)

| Tabla en PostgreSQL (`__tablename__`) | Archivo donde está definida |
|--------------------------------------|-----------------------------|
| `roles` | `API/database/rol.py` |
| `direcciones` | `API/database/direccion.py` |
| `usuarios` | `API/database/usuario.py` |
| `categorias` | `API/database/categoria.py` |
| `marcas` | `API/database/marca.py` |
| `autopartes` | `API/database/autoparte.py` |
| `inventarios` | `API/database/inventario.py` |
| `estatus_pedido` | `API/database/estatus_pedido.py` |
| `pedidos` | `API/database/pedido.py` |
| `detalles_pedidos` | `API/database/detalle_pedido.py` |

**Orden de creación:** lo resuelve SQLAlchemy según **claves foráneas** entre modelos (por ejemplo `usuarios` depende de `roles` y opcionalmente de `direcciones`; `pedidos` de `usuarios`, `estatus_pedido`, `direcciones`; etc.). No hace falta un orden manual si todos los modelos están importados en `API/database/__init__.py` antes del `create_all`.

### Cómo esas tablas “llegan” a PostgreSQL en tu máquina

En el script raíz `setup.sh`, después de levantar Docker, se ejecuta (resumido):

```bash
docker exec macuin_api python -c "
from database.db import engine, Base
from database import *
Base.metadata.create_all(bind=engine)
"
```

Eso crea las tablas en la base **`DB_macuin`** del contenedor Postgres. Desde el host, la extensión **Database Client** / JDBC suele conectarse con:

- Host: `127.0.0.1`
- Puerto: `5433` (mapeado en `docker-compose.yml`)
- Base: `DB_macuin`
- Usuario / contraseña: los definidos en `docker-compose.yml` (`macuin` / `123456`)

### Laravel y la misma base (importante)

Laravel tiene sus propias migraciones en `Laravel/database/migrations/` (por ejemplo tabla `users`, `sessions`, etc.). Eso es **otro conjunto de tablas** que puede convivir en la misma base `DB_macuin` si ejecutas `php artisan migrate`, pero hay que **planificar** para no duplicar conceptos de negocio sin criterio (por ejemplo `users` del portal vs `usuarios` de la API).

---

## FASE 1 — Base de datos (PostgreSQL)

**Objetivo:** Tener PostgreSQL operativo, esquema de tablas de la API creado y visible (JDBC / cliente SQL), y criterio claro respecto a migraciones Laravel.

**Tareas recomendadas:**

1. Levantar el stack con Docker (`docker compose` o `bash setup.sh` si tu entorno lo permite).
2. Verificar que `create_all` se ejecutó sin error (logs del contenedor `macuin_api` o ejecutar el bloque Python manualmente dentro del contenedor).
3. En el cliente gráfico, comprobar el esquema `public`: deben aparecer las tablas listadas arriba.
4. Decidir si en esta fase también se ejecutan migraciones de Laravel sobre `DB_macuin` y en qué orden (API primero suele ser lo habitual para no romper FKs si algún día unificáis datos).
5. Opcional: datos semilla (roles, estatus de pedido, categorías base) vía script SQL, seeder o endpoints admin — según acuerdo del equipo.

**Criterio de “FASE 1 lista”:** Conexión estable a PostgreSQL y tablas de la API presentes y coherentes con los modelos en `API/database/`.

**Inicialización unificada:** en el contenedor `macuin_api`, ejecuta `python scripts/init_db.py` (crea tablas faltantes y aplica el seed mínimo si `roles` está vacío). El inventario documentado de tablas y cobertura por módulo está en **`TABLAS_PROYECTO.md`** (raíz del repo; en Ctrl+P escribe `TABLAS`). Resumen de redirección: `API/database/TABLAS_PROYECTO.md`.

---

## FASE 2 — API FastAPI (`API/`)

**Objetivo:** Backend REST estable, documentado en `/docs`, alineado con el esquema creado en la FASE 1.

**Tareas recomendadas:**

1. Revisar cada router en `API/router/` frente a las pantallas que consumirán la API (Flask y, si aplica, Laravel).
2. Completar validaciones, códigos HTTP y manejo de errores.
3. Definir autenticación/autorización si los módulos internos deben estar protegidos (tokens, sesión, etc.).
4. Pruebas manuales o automatizadas contra la base real (no solo mocks).

**Criterio de “FASE 2 lista”:** Los flujos críticos de negocio (usuarios internos, catálogo, inventario, pedidos, direcciones) tienen endpoints probados contra PostgreSQL.

---

## FASE 3 — Flask (`Flask/`)

**Objetivo:** La interfaz web por roles deja de depender de datos en memoria y formularios “vacíos”, y persiste/consulta vía API.

**Situación actual (referencia):** En `Flask/routes.py` hay un diccionario `USUARIOS` para login y muchos comentarios del tipo “Aquí se conectará con el API”; los dashboards muestran KPIs fijos en HTML.

**Tareas recomendadas:**

1. Cliente HTTP desde Flask hacia la URL de la API (variable de entorno, p. ej. en Docker la red interna).
2. Sustituir login simulado por flujo real acordado (validación contra API o servicio de auth).
3. Implementar cada `POST`/`PATCH`/`GET` necesario en las rutas que hoy solo redirigen.
4. Pasar datos reales a las plantillas (`templates/`).

**Criterio de “FASE 3 lista”:** Un usuario de cada rol puede completar las acciones principales del módulo y los datos se reflejan en la base vía API.

---

## FASE 4 — Laravel (`Laravel/`)

**Objetivo:** Portal de clientes (y rutas asociadas) con datos reales; auth y pedidos alineados con la estrategia global.

**Situación actual (referencia):** Varias vistas usan arrays PHP en Blade (catálogo falso); rutas como `/catalogo` o `/pedidos` devuelven vistas sin controlador con datos de BD.

**Tareas recomendadas:**

1. Conectar catálogo, carrito, pedidos y pago a la fuente de verdad (API o Eloquent, según decisión de arquitectura).
2. Mantener coherente el modelo `users` de Laravel con el registro/login y con los pedidos.
3. Revisar la entrada “personal” que redirige vía `API_BASE_URL` (`/v1/redirect/personal` hacia Flask).
4. Ajustar `.env` para desarrollo local vs Docker (`DB_HOST`, `DB_PORT`, `API_BASE_URL`, `FLASK_URL`).

**Criterio de “FASE 4 lista”:** Flujo de cliente (registro/login, ver catálogo, carrito, ver pedidos) funcional con datos persistentes.

---

## FASE 5 — Integración extremo a extremo

**Objetivo:** Los tres frentes (API, Flask, Laravel) y una sola base coordinada se comportan como un solo sistema.

**Tareas recomendadas:**

1. Matriz de flujos: qué actor usa qué URL y qué servicio toca.
2. Variables de entorno documentadas para cada contenedor y para desarrollo fuera de Docker.
3. Pruebas de regresión en Docker (compose completo).
4. Revisión de CORS, URLs absolutas y puertos publicados (`8000`, `5001`, `8003`, `5433`).

**Criterio de “FASE 5 lista”:** Casos de uso acordados pasan de punta a punta sin pasos manuales no documentados.

---

## FASE 6 — Calidad, seguridad y entrega

**Objetivo:** Proyecto entregable en sentido profesional.

**Tareas recomendadas:**

1. Secretos: no versionar contraseñas reales; rotar las de ejemplo en entornos compartidos.
2. `APP_DEBUG`, logs y mensajes de error aptos para producción.
3. Copias de seguridad de PostgreSQL y procedimiento de restauración.
4. README operativo para quien despliegue (puede seguir complementándose con `README.md` y `README_DOCKER.md`).

**Criterio de “FASE 6 lista”:** Checklist de entrega cumplida y documentación suficiente para operar y mantener el sistema.

---

## Extensiones recomendadas en el workspace

En la raíz del repo, `.vscode/extensions.json` recomienda **Database Client** y **Database Client JDBC** para trabajar el panel *Database* como en tu flujo de trabajo habitual.

---

## Resumen rápido

| Si quieres… | Ve a… |
|-------------|--------|
| Ver **nombres y columnas** de las tablas de la FASE 1 | `API/database/*.py` (cada `__tablename__`) |
| Ver **qué modelos se incluyen** al crear tablas | `API/database/__init__.py` |
| Ver **cadena de conexión** | `API/database/db.py` y variables en `docker-compose.yml` |
| Ver **cómo se disparan** las tablas en Postgres | `setup.sh` (bloque `docker exec macuin_api python -c ...`) |

---

*Documento generado para alinear el trabajo por fases del proyecto Macuin.*
