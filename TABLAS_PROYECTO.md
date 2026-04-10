# Tablas del proyecto Macuin (PostgreSQL — FASE 1)

Este archivo está en la **raíz del repositorio** para encontrarlo fácil en Cursor/VS Code.

## Cómo abrirlo y el resto de la FASE 1 en el editor

1. Pulsa **Ctrl+P** (abrir archivo rápido).
2. Escribe solo: **`TABLAS`** o **`TABLAS_PROYECTO`** y elige `TABLAS_PROYECTO.md`.
3. **No** incluyas el nombre de la carpeta padre (`Macuin/…`). La raíz del workspace ya es tu proyecto (por ejemplo `MACUIN` o `GitHub/Macuin`); las rutas correctas empiezan por `API/…`, `Flask/…`, etc.

### Otros archivos clave de la FASE 1 (mismo truco: Ctrl+P)

| Qué buscar | Ruta real |
|------------|-----------|
| Modelos SQLAlchemy | `API/database/__init__.py` luego cada `API/database/*.py` |
| Conexión a Postgres | `API/database/db.py` |
| Crear tablas + seed | `API/scripts/init_db.py` |
| Datos iniciales | `API/database/seed_fase1.py` |
| Setup Docker | `setup.sh` (llama a `init_db` en el contenedor API) |

---

## Ver las tablas en “Database Client” / JDBC (como tu captura)

### 1) Qué extensiones hacen falta (importante)

- El panel lateral **“Database”** lo registra la extensión principal **Database Client** (`cweijan.vscode-database-client2` en Marketplace).
- **Database Client JDBC** (`cweijan.dbclient-jdbc`) es un **complemento** para otros motores por JDBC; **sola no crea** el icono ni el árbol de conexiones.

En el repo ya están recomendadas en `.vscode/extensions.json`. Puedes reinstalarlas desde terminal (Cursor en Windows):

```powershell
cursor --install-extension cweijan.vscode-database-client2 --force
cursor --install-extension cweijan.dbclient-jdbc --force
```

(O ejecuta el script `scripts/instalar-database-client-cursor.ps1` en la raíz del proyecto.)

Después: **Ctrl+Shift+P** → **Developer: Reload Window** (recargar ventana).

### 2) Si no ves el icono del cilindro “Database” en la barra lateral

En Cursor a veces el icono queda oculto o hace falta activar la vista:

1. **Clic derecho** sobre la **barra de actividades** (la columna de iconos a la izquierda) y revisa si **Database** está desmarcado; márcalo.
2. Si hay **más iconos** abajo (`…` / “Views and more actions”), ábrelo: a veces las extensiones quedan ahí.
3. **Menú Ver:** `View` → `Appearance` → comprueba que la **Activity Bar** esté visible.
4. Abrir el panel por comando interno de VS Code/Cursor: **Ctrl+Shift+P** → pega y ejecuta:
   - `View: Open View...` → escribe **Database** y elige la vista del contenedor **Database** (MySQL / Database Client).
   - Si no aparece, prueba el id de contenedor: ejecuta **Preferences: Open Keyboard Shortcuts (JSON)** solo para consultar; la vista suele registrarse como contenedor `github-cweijan-mysql`. En la paleta también puedes buscar **MySQL** o **Add Connection** (categoría MySQL en comandos de la extensión).

Cuando el panel **Database** esté abierto:

1. **Add Connection** (+) → **PostgreSQL**.
2. Datos alineados con `docker-compose.yml` (conexión **desde tu PC** al contenedor):

   - **Host:** `127.0.0.1`
   - **Puerto:** `5433` (mapeo host → 5432 en el contenedor)
   - **Base de datos:** `DB_macuin`
   - **Usuario:** `macuin`
   - **Contraseña:** `123456`

3. URL JDBC típica: `jdbc:postgresql://127.0.0.1:5433/DB_macuin`
4. Docker con `postgres` en marcha. Si **Tables** está vacío:  
   `docker exec macuin_api python scripts/init_db.py`

> **Nota:** No se puede “empaquetar” la extensión dentro del código del proyecto Git: vive en el editor. Lo que sí hace el proyecto es recomendarla (`.vscode/extensions.json`), documentarla aquí y ofrecer el script de instalación por CLI.

---

## Qué resume este documento

Todas las tablas que crea SQLAlchemy (`Base.metadata.create_all`) a partir de los archivos en `API/database/`. Las columnas detalladas están en cada `.py`; aquí tienes el mapa general.

**Regenerar tablas / seed:** dentro del contenedor `macuin_api`:

```bash
python scripts/init_db.py
```

---

## Cobertura por interfaz (resumen de auditoría)

| Área | Interfaz / módulo | Tablas que soportan los datos |
|------|-------------------|------------------------------|
| Personal interno | Flask login (futuro: API) | `roles`, `usuarios` |
| Admin | Usuarios internos, catálogo, pedidos, configuración | `usuarios`, `roles`, `autopartes`, `categorias`, `marcas`, `pedidos`, `detalles_pedidos`, `estatus_pedido`, `parametros_sistema` |
| Ventas | Clientes, pedidos, catálogo lectura | `clientes`, `direcciones`, `pedidos`, `detalles_pedidos`, `autopartes`, … |
| Logística | Envíos, direcciones lectura, guías | `pedidos`, `estatus_pedido`, `direcciones`, `guias_envio` |
| Almacén | Inventario, ubicaciones, pedidos, autopartes lectura | `inventarios`, `movimientos_inventario`, `ubicaciones`, `pedidos`, `autopartes` |
| Portal cliente | Laravel catálogo, carrito, pedidos, pago (fases siguientes) | `autopartes`, `categorias`, `marcas`, `carritos`, `carrito_lineas`, `pagos`, `pedidos` (cuando se integre) |

---

## Lista de tablas y archivos fuente (`API/database/`)

| Tabla | Archivo |
|-------|---------|
| `roles` | `rol.py` |
| `clientes` | `cliente.py` |
| `direcciones` | `direccion.py` |
| `usuarios` | `usuario.py` |
| `categorias` | `categoria.py` |
| `marcas` | `marca.py` |
| `autopartes` | `autoparte.py` |
| `ubicaciones` | `ubicacion.py` |
| `inventarios` | `inventario.py` |
| `estatus_pedido` | `estatus_pedido.py` |
| `pedidos` | `pedido.py` |
| `detalles_pedidos` | `detalle_pedido.py` |
| `guias_envio` | `guia_envio.py` |
| `movimientos_inventario` | `movimiento_inventario.py` |
| `parametros_sistema` | `parametro_sistema.py` |
| `carritos` | `carrito.py` |
| `carrito_lineas` | `carrito.py` |
| `pagos` | `pago.py` |

Además, **Laravel** puede crear en la misma base tablas como `users`, `sessions`, `migrations`, etc., si ejecutaste `php artisan migrate`.

---

## Relaciones principales (texto)

- **Cliente** 1—N **Direcciones** (`direcciones.cliente_id`).
- **Usuario** (interno) N—1 **Rol**; opcional dirección empleado.
- **Autoparte** N—1 **Categoría**, N—1 **Marca**; 1—1 **Inventario** (por `autoparte_id` único).
- **Inventario** opcional N—1 **Ubicación**; 1—N **Movimientos_inventario** (entradas/mermas).
- **Pedido** N—1 **Usuario**, N—1 **Estatus**, N—1 **Dirección** de envío, opcional N—1 **Cliente**; 1—N **Detalles_pedido**; 1—N **Guías_envio**.
- **Detalle_pedido** N—1 **Pedido**, N—1 **Autoparte**; columna generada `subtotal` (PostgreSQL).
- **Carrito** 1—N **Carrito_lineas**; cada línea N—1 **Autoparte**. `laravel_user_id` sin FK a `users` para no depender del orden de migraciones.

---

## Seed FASE 1 (`API/database/seed_fase1.py`)

Si `roles` está vacío, se insertan roles (Administrador, Ventas, Logística, Almacén), estatus de flujo (Borrador … Cancelado) y el usuario **sistema@macuin.local** (hash marcador; cambiar antes de producción).

---

## Notas importantes

1. **`create_all` no altera columnas** en tablas ya existentes: migración manual, Alembic o volumen limpio si cambias modelos sobre una BD vieja.
2. Documentación interactiva de la API: `http://localhost:8000/docs` con el contenedor `api` en marcha.
