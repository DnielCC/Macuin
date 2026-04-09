## VENTAS

# Templates agregados
Se agregaron las siguientes plantillas en `Flask/templates/`:

- `ventas_reportes.html` → Reportes del departamento de Ventas
  - **Reporte de Pedidos**: tabla con folio, cliente, total, estatus y % del ingreso total.
    Permite descargar en PDF, Excel y Word con resumen ejecutivo y firma del usuario.
  - **Reporte de Clientes**: lista completa de clientes con indicador de activos/inactivos.
- `ventas_catalogo.html` → Catálogo de autopartes visible para Ventas
- `ventas_clientes.html` → Gestión de clientes
- `ventas_pedidos.html` → Gestión de pedidos
- `ventas_dashboard.html` → Dashboard del módulo de Ventas
  - Se agregó acceso rápido a **Reportes** en la sección "Accesos Rápidos" apuntando a `/ventas/reportes`

# Rutas agregadas en routes.py
Se agregaron las siguientes rutas en `Flask/routes.py`:

- `GET /ventas/reportes` → función `ventas_reportes()` — acceso restringido al rol Ventas
- `GET /ventas/catalogo` → función `ventas_catalogo()`
- `GET /ventas/clientes` → función `ventas_clientes()`
- `GET /ventas/pedidos` → función `ventas_pedidos()`
- `GET /ventas/dashboard` → función `ventas_dashboard()`

Se creó la función auxiliar `solo_ventas()` que valida login y rol antes de cada ruta del módulo.

# Corrección de bug
En `ventas_reportes.html` línea 392, la función `descargarWord()` tenía un paréntesis
de cierre extra en la construcción de `tablaDetalle` (D.Table de docx.js).

```js
//  Antes
...margins:{top:100,bottom:100,left:100,right:100}}))})),...body.map(

// Después
...margins:{top:100,bottom:100,left:100,right:100}}}))}),...body.map(
```

---

## LOGÍSTICA

# Templates agregados
Se agregaron las siguientes plantillas en `Flask/templates/`:

- `logistica_reportes.html` → Reportes del departamento de Logística
  - **Reporte de Envíos**: todos los pedidos del período con dirección de entrega y estatus.
  - **Reporte por Estatus**: tabla agrupada con cantidad de pedidos por estatus y tasa de entrega.
    Permite descargar en PDF, Excel y Word con el mismo formato profesional que Admin.
- `logistica_envios.html` → Gestión de envíos
- `logistica_guias.html` → Gestión de guías
- `logistica_direcciones.html` → Gestión de direcciones
- `logistica_dashboard.html` → Dashboard del módulo de Logística
  - Se agregó acceso rápido a **Reportes** en la sección "Accesos Rápidos" apuntando a `/logistica/reportes`

# Rutas agregadas en routes.py
Se agregaron las siguientes rutas en `Flask/routes.py`:

- `GET /logistica/reportes` → función `logistica_reportes()` — acceso restringido al rol Logística
- `GET /logistica/envios` → función `logistica_envios()`
- `GET /logistica/guias` → función `logistica_guias()`
- `GET /logistica/direcciones` → función `logistica_direcciones()`
- `GET /logistica/dashboard` → función `logistica_dashboard()`

Se creó la función auxiliar `solo_logistica()` que valida login y rol antes de cada ruta del módulo.

# Corrección de bug
En `logistica_reportes.html` línea 411, la función `descargarWord()` tenía el mismo
paréntesis extra que en ventas_reportes. Se corrigió de la misma manera.