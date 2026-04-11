-- =============================================================================
-- Repara textos con tildes / eñes que quedaron como ?? al cargar el seed SQL
-- con una codificación incorrecta (p. ej. Get-Content sin UTF-8 en Windows).
-- Idempotente: puedes ejecutarlo varias veces.
--
--   .\scripts\ejecutar_seed_datos_reales.ps1 -SqlFile reparar_textos_utf8_datos_reales.sql
-- =============================================================================

SET client_encoding TO 'UTF8';

BEGIN;

-- Roles usados en login (session user_role) — localizados por email de usuario demo
UPDATE roles r
SET nombre_rol = 'Administrador',
    descripcion = 'Acceso total al sistema y catálogo maestro.'
FROM usuarios u
WHERE u.email = 'admin@macuin.com' AND u.rol_id = r.id;

UPDATE roles r
SET nombre_rol = 'Ventas',
    descripcion = 'Clientes B2B y pedidos.'
FROM usuarios u
WHERE u.email = 'ventas@macuin.com' AND u.rol_id = r.id;

UPDATE roles r
SET nombre_rol = 'Logística',
    descripcion = 'Envíos, guías y estatus de entrega.'
FROM usuarios u
WHERE u.email = 'logistica@macuin.com' AND u.rol_id = r.id;

UPDATE roles r
SET nombre_rol = 'Almacén',
    descripcion = 'Inventario, ubicaciones y surtido.'
FROM usuarios u
WHERE u.email = 'almacen@macuin.com' AND u.rol_id = r.id;

-- Usuarios demo (API/scripts/seed_macuin_demo_users.py)
UPDATE usuarios SET nombre = 'Frank', apellidos = 'Contreras' WHERE email = 'admin@macuin.com';
UPDATE usuarios SET nombre = 'María', apellidos = 'González' WHERE email = 'ventas@macuin.com';
UPDATE usuarios SET nombre = 'Ana', apellidos = 'Martínez' WHERE email = 'logistica@macuin.com';
UPDATE usuarios SET nombre = 'Carlos', apellidos = 'López' WHERE email = 'almacen@macuin.com';

-- Categorías (por SKU de catálogo demo; no depende del nombre corrupto actual)
UPDATE categorias c SET nombre = 'Frenos' FROM autopartes a WHERE a.sku_codigo = 'MU-FR-001' AND a.categoria_id = c.id;
UPDATE categorias c SET nombre = 'Suspensión' FROM autopartes a WHERE a.sku_codigo = 'MU-SU-001' AND a.categoria_id = c.id;
UPDATE categorias c SET nombre = 'Filtros' FROM autopartes a WHERE a.sku_codigo = 'MU-FI-001' AND a.categoria_id = c.id;
UPDATE categorias c SET nombre = 'Sistema eléctrico' FROM autopartes a WHERE a.sku_codigo = 'MU-EL-001' AND a.categoria_id = c.id;
UPDATE categorias c SET nombre = 'Motor' FROM autopartes a WHERE a.sku_codigo = 'MU-MO-001' AND a.categoria_id = c.id;

-- Marcas (mismo criterio)
UPDATE marcas m SET nombre = 'TRW' FROM autopartes a WHERE a.sku_codigo = 'MU-FR-001' AND a.marca_id = m.id;
UPDATE marcas m SET nombre = 'Bosch' FROM autopartes a WHERE a.sku_codigo = 'MU-FR-002' AND a.marca_id = m.id;
UPDATE marcas m SET nombre = 'Monroe' FROM autopartes a WHERE a.sku_codigo = 'MU-SU-001' AND a.marca_id = m.id;
UPDATE marcas m SET nombre = 'TRW' FROM autopartes a WHERE a.sku_codigo = 'MU-SU-002' AND a.marca_id = m.id;
UPDATE marcas m SET nombre = 'Mann-Filter' FROM autopartes a WHERE a.sku_codigo = 'MU-FI-001' AND a.marca_id = m.id;
UPDATE marcas m SET nombre = 'Bosch' FROM autopartes a WHERE a.sku_codigo = 'MU-FI-002' AND a.marca_id = m.id;
UPDATE marcas m SET nombre = 'NGK' FROM autopartes a WHERE a.sku_codigo = 'MU-EL-001' AND a.marca_id = m.id;
UPDATE marcas m SET nombre = 'Bosch' FROM autopartes a WHERE a.sku_codigo = 'MU-EL-002' AND a.marca_id = m.id;
UPDATE marcas m SET nombre = 'Bosch' FROM autopartes a WHERE a.sku_codigo = 'MU-MO-001' AND a.marca_id = m.id;
UPDATE marcas m SET nombre = 'TRW' FROM autopartes a WHERE a.sku_codigo = 'MU-MO-002' AND a.marca_id = m.id;

-- Autopartes (texto canónico del seed_datos_reales_macuin.sql)
UPDATE autopartes SET nombre = 'Pastillas de freno cerámicas delanteras', descripcion = 'Bajo polvo; SUV y pick-up.' WHERE sku_codigo = 'MU-FR-001';
UPDATE autopartes SET nombre = 'Disco de freno ventilado 280 mm', descripcion = 'Par delantero recomendado.' WHERE sku_codigo = 'MU-FR-002';
UPDATE autopartes SET nombre = 'Amortiguador delantero a gas', descripcion = 'Con anclaje estándar MacPherson.' WHERE sku_codigo = 'MU-SU-001';
UPDATE autopartes SET nombre = 'Kit bieletas de barra estabilizadora', descripcion = 'Incluye tornillería.' WHERE sku_codigo = 'MU-SU-002';
UPDATE autopartes SET nombre = 'Filtro de aceite spin-on', descripcion = 'Alta retención de partículas.' WHERE sku_codigo = 'MU-FI-001';
UPDATE autopartes SET nombre = 'Aceite sintético 5W-30 4 L', descripcion = 'API SP / ILSAC GF-6.' WHERE sku_codigo = 'MU-FI-002';
UPDATE autopartes SET nombre = 'Bujía de encendido iridium', descripcion = 'Motor gasolina eficiente.' WHERE sku_codigo = 'MU-EL-001';
UPDATE autopartes SET nombre = 'Sensor MAP', descripcion = 'Presión absoluta multicanal.' WHERE sku_codigo = 'MU-EL-002';
UPDATE autopartes SET nombre = 'Kit de correa de distribución', descripcion = 'Incluye tensor y polea.' WHERE sku_codigo = 'MU-MO-001';
UPDATE autopartes SET nombre = 'Termostato 87 °C', descripcion = 'Sellado OEM equivalente.' WHERE sku_codigo = 'MU-MO-002';

-- Clientes B2B demo
UPDATE clientes SET nombre = 'Taller Mecánico del Norte SA', notas = 'Compra recurrente: frenos y suspensión.' WHERE email = 'b2b.taller.norte@macuin.demo';
UPDATE clientes SET nombre = 'Refaccionaria Central del Bajío', notas = 'Surtido mixto; picos en fin de mes.' WHERE email = 'b2b.refacciones.central@macuin.demo';
UPDATE clientes SET nombre = 'Transportes y Servicios López', notas = 'Flotilla; consumibles eléctricos.' WHERE email = 'b2b.transportes.lopez@macuin.demo';

-- Ubicaciones almacén
UPDATE ubicaciones SET descripcion = 'Rack principal — piezas de frenado' WHERE pasillo = 'A' AND estante = '01' AND COALESCE(nivel, '') = '1';
UPDATE ubicaciones SET descripcion = 'Suspensión y dirección' WHERE pasillo = 'A' AND estante = '02' AND COALESCE(nivel, '') = '2';
UPDATE ubicaciones SET descripcion = 'Componentes eléctricos ESD' WHERE pasillo = 'B' AND estante = '01' AND COALESCE(nivel, '') = '1';

-- Direcciones (por cliente + CP del seed)
UPDATE direcciones d SET
  calle_principal = 'Av. Insurgentes Sur',
  num_ext = '2400',
  num_int = NULL,
  colonia = 'Del Valle',
  municipio = 'Ciudad de México',
  estado = 'CDMX',
  referencias = 'Recepción B2B'
FROM clientes c
WHERE c.email = 'b2b.taller.norte@macuin.demo' AND d.cliente_id = c.id AND d.cp = '03100';

UPDATE direcciones d SET
  calle_principal = 'Blvd. López Mateos',
  num_ext = '1805',
  num_int = 'B',
  colonia = 'Jardines del Moral',
  municipio = 'León',
  estado = 'Guanajuato',
  referencias = 'Andén 2'
FROM clientes c
WHERE c.email = 'b2b.refacciones.central@macuin.demo' AND d.cliente_id = c.id AND d.cp = '37180';

UPDATE direcciones d SET
  calle_principal = 'Calzada Ignacio Zaragoza',
  num_ext = '422',
  num_int = NULL,
  colonia = '4 Árboles',
  municipio = 'Ciudad de México',
  estado = 'CDMX',
  referencias = '9–14 h'
FROM clientes c
WHERE c.email = 'b2b.transportes.lopez@macuin.demo' AND d.cliente_id = c.id AND d.cp = '15730';

COMMIT;
