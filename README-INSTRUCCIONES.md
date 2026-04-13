# Guía de entrega — Rúbrica 3er parcial (TAI)

Este documento enlaza **cada criterio de la rúbrica** con **rutas, archivos y qué mostrar** al presentar el proyecto (navegador, Swagger, código y contenedores).

**Raíz del repositorio:** carpeta `Macuin/` (donde está `docker-compose.yml`).

---

## 1. Dos frontends (uno asociado a la API y otro en Laravel)

- **Panel interno (Flask)**
  - **Dónde:** carpeta `Flask/`; en Docker, servicio `flask` y puerto **5001** (ver `docker-compose.yml`).
  - **Qué mostrar:** abrir `http://localhost:5001`, iniciar sesión como personal (Administrador, Ventas, Logística o Almacén) y comentar que las pantallas consumen la API (no ejecutan SQL directo desde Flask).

- **Portal cliente (Laravel)**
  - **Dónde:** carpeta `Laravel/`; en Docker, puerto **8003**.
  - **Qué mostrar:** abrir `http://localhost:8003` (selector, registro, catálogo, carrito, pedidos). La rúbrica suele citar “Laravel 8”; la versión instalada del framework está en `Laravel/composer.json` (`laravel/framework`).

- **Archivos de referencia rápida**
  - Flask: `Flask/main.py`, `Flask/routes/`, `Flask/services/api.py` (cliente HTTP hacia FastAPI).
  - Laravel: `Laravel/routes/web.php`, `Laravel/app/Http/Controllers/`.

---

## 2. Toda la lógica de negocio en una API FastAPI

- **Aplicación y configuración**
  - **Dónde:** `API/main.py` (app FastAPI, CORS, registro de routers).
  - **Qué mostrar:** documentación interactiva en `http://localhost:8000/docs` (Swagger).

- **Endpoints por módulo**
  - **Dónde:** `API/router/*.py` (cada archivo agrupa rutas por dominio).
  - **Qué mostrar:** en Swagger, desplegar los distintos tags (pedidos, autopartes, reportes, etc.).

---

## 3. Carpetas de la API organizadas con `router` para los endpoints

- **Routers**
  - **Dónde:** carpeta `API/router/`.
  - **Qué mostrar:** listar el contenido de `API/router/` en el IDE o terminal y abrir `API/main.py` donde aparecen las líneas `app.include_router(...)`.

---

## 4. Modelos SQLAlchemy para la base de datos

- **Modelos ORM**
  - **Dónde:** `API/database/*.py` (definición de tablas con SQLAlchemy).
  - **Qué mostrar:** abrir por ejemplo `API/database/pedido.py` y `API/database/autoparte.py`.

- **Sesión y conexión**
  - **Dónde:** `API/database/db.py`.
  - **Qué mostrar:** cómo se usa `get_db` y que la URL de base de datos viene de `DATABASE_URL` en el entorno Docker.

---

## 5. La API como punto principal de acceso a la base de datos

- **Lectura y escritura vía API**
  - **Dónde:** routers que usan `Depends(get_db)`.
  - **Qué mostrar:** en Swagger, ejecutar un GET o POST que devuelva datos reales de la base.

- **Nota sobre Laravel**
  - **Dónde:** `Laravel` comparte la misma PostgreSQL definida en `docker-compose.yml` (variables `DB_*` del servicio `laravel`). Algunas pantallas (por ejemplo el listado de pedidos del cliente) leen con Eloquent en `Laravel/app/Models/Macuin/`.
  - **Qué decir si preguntan:** la **lógica y el CRUD principal** del sistema están en **FastAPI**; el portal puede leer tablas compartidas para ciertas vistas.

---

## 6. Componentes en contenedores Docker

- **Orquestación**
  - **Dónde:** `docker-compose.yml`.
  - **Contenido relevante:** servicios `postgres`, `api`, `flask`, `laravel`.

- **Qué mostrar en terminal**
  - Ejecutar `docker compose ps` y ver los cuatro servicios en estado *running* / *up*.

---

## 7. Registro de usuarios externos (front → API → BD)

- **Flujo en el portal**
  - **Dónde:** `Laravel/routes/web.php` (rutas de registro), `Laravel/app/Http/Controllers/Auth/RegisteredUserController.php`.
  - **Qué mostrar:** pantalla de registro en Laravel y que el usuario o la fila en `clientes` quede reflejada en la base (o en listados vía API, según el flujo que demuestren).

- **API de clientes**
  - **Dónde:** `API/router/clientes.py`.
  - **Qué mostrar:** endpoints bajo `/v1/clientes/` en Swagger para el ciclo de clientes en la API.

---

## 8. Pedido con 1 a N productos (endpoint)

- **Cabecera del pedido**
  - **Dónde:** `API/router/pedidos.py` — `POST /v1/pedidos/`.
  - **Qué mostrar:** crear un pedido (cabecera).

- **Líneas (varios productos)**
  - **Dónde:** mismo archivo — `POST /v1/pedidos/{pedido_id}/detalles` (cuerpo con `autoparte_id`, `cantidad`, etc.); modelo en `API/models/detalle_pedido.py`.
  - **Qué mostrar:** en Swagger, un mismo pedido con **varias** líneas de detalle.

---

## 9. Consultar todos los pedidos del usuario

- **Vista en el portal Laravel**
  - **Dónde:** `Laravel/app/Http/Controllers/PedidosController.php`, ruta `pedidos` en `Laravel/routes/web.php`, vista en `Laravel/resources/views/` (p. ej. `pedidos.blade.php` si existe).
  - **Qué mostrar:** usuario autenticado en `/pedidos`, listado filtrado por el cliente vinculado a su correo.

- **API (listados generales o admin)**
  - **Dónde:** `GET /v1/pedidos/` y `GET /v1/pedidos/admin/vista` en `API/router/pedidos.py`.
  - **Qué mostrar:** respuesta en Swagger o pantalla equivalente en Flask (módulo de pedidos admin).

---

## 10. CRUD de usuarios internos

- **API**
  - **Dónde:** `API/router/usuarios.py` — prefijo `/v1/usuarios` (GET lista, GET por id, POST, PUT, DELETE con autenticación donde corresponda).
  - **Qué mostrar:** Swagger con al menos un ejemplo de POST o PUT.

- **Panel Flask**
  - **Dónde:** rutas y plantillas de administración de usuarios (buscar en `Flask/routes/` referencias a `admin_usuarios` o similares).
  - **Qué mostrar:** pantalla CRUD en el navegador.

---

## 11. CRUD de autopartes

- **API**
  - **Dónde:** `API/router/autopartes.py` — rutas bajo `/v1/autopartes`.
  - **Qué mostrar:** en Swagger, alta, edición, baja y listado.

- **Panel**
  - **Dónde:** Flask — módulo de catálogo admin (`Flask/routes/` y `Flask/templates/` relacionados con catálogo).
  - **Qué mostrar:** operaciones completas desde la interfaz.

---

## 12. Mínimo cuatro tipos de reportes (endpoints)

Los cuatro tipos están bajo el prefijo **`/v1/reportes`** en `API/router/reportes.py`. Registro del router en `API/main.py` (`app.include_router(reportes.router_reportes)`).

1. **Pedidos** — `GET /v1/reportes/pedidos`
2. **Catálogo de autopartes** — `GET /v1/reportes/catalogo-autopartes`
3. **Usuarios internos** — `GET /v1/reportes/usuarios-internos`
4. **Inventario y almacén** — `GET /v1/reportes/inventario-almacen`

**Qué mostrar:** en `http://localhost:8000/docs`, ejecutar los cuatro GET y mostrar el JSON (`tipo_reporte`, `filas`, etc.).

---

## 13. Reportes descargables en PDF, Word (.docx) y Excel (.xlsx)

- **Pantalla de reportes**
  - **Dónde:** tras login en Flask, ruta **`/reportes`** (menú **Reportes**).
  - **Qué mostrar:** cuatro tarjetas (una por tipo de reporte); en cada una, pulsar **PDF**, **Word** y **Excel** y abrir los archivos descargados.

- **Ruta y parámetros**
  - **Dónde:** `Flask/routes/reportes_segment.py` — `POST /reportes/descargar`.
  - **Detalle:** formulario con `preset` (tipo de reporte) y `fmt` (`pdf`, `docx`, `xlsx`).

- **Generación de archivos**
  - **Dónde:** `Flask/services/reports.py` — funciones `render_pdf`, `render_docx`, `render_xlsx` y diccionario `REPORT_PRESETS`.
  - **Qué explicar:** los datos se arman con `build_report_context` usando `Flask/services/api.py` contra la API.

- **Dependencias**
  - **Dónde:** `Flask/requirements.txt` — paquetes `reportlab`, `python-docx`, `openpyxl`.
  - **Uso:** si preguntan por el stack de exportación a archivos.

**Permisos por rol (resumen):**

- **Pedidos** y **Catálogo:** Administrador, Ventas, Logística, Almacén.
- **Usuarios internos:** solo Administrador.
- **Inventario y almacén:** Administrador y Almacén.

Para la demo ante el docente, conviene entrar como **Administrador** y descargar los cuatro tipos en los tres formatos.

---

## Resumen rápido de URLs (desarrollo local con Docker)

- **API (Swagger):** http://localhost:8000/docs
- **Panel Flask:** http://localhost:5001
- **Portal Laravel:** http://localhost:8003
- **PostgreSQL desde el host:** puerto **5433** (mapeo en `docker-compose.yml`)

---

*Documento para alinear la entrega con la rúbrica del 3er parcial. Ajusta capturas o guion oral según lo que pida tu docente.*
