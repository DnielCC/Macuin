-- =============================================================================
-- MACUIN — 10 sentencias INSERT con datos coherentes para catálogo, reportes
-- y gráficas. NO inserta en usuarios.
--
-- Requisitos: init_db + seed_fase1 + seed_macuin_demo_users (ventas@macuin.com).
--
--   docker exec -i macuin_db psql -U macuin -d DB_macuin < scripts/seed_datos_reales_macuin.sql
--   psql -h 127.0.0.1 -p 5433 -U macuin -d DB_macuin -f scripts/seed_datos_reales_macuin.sql
-- =============================================================================

BEGIN;

-- [1/10] Categorías
INSERT INTO categorias (nombre) VALUES
  ('Frenos'),
  ('Suspensión'),
  ('Filtros'),
  ('Sistema eléctrico'),
  ('Motor')
ON CONFLICT (nombre) DO NOTHING;

-- [2/10] Marcas
INSERT INTO marcas (nombre) VALUES
  ('Bosch'),
  ('TRW'),
  ('Monroe'),
  ('NGK'),
  ('Mann-Filter')
ON CONFLICT (nombre) DO NOTHING;

-- [3/10] Ubicaciones de almacén (3 filas; idempotente fila a fila)
INSERT INTO ubicaciones (pasillo, estante, nivel, capacidad, descripcion, activo)
SELECT u.pasillo, u.estante, u.nivel, u.capacidad, u.descripcion, u.activo
FROM (VALUES
  ('A', '01', '1', 800,  'Rack principal — piezas de frenado', true),
  ('A', '02', '2', 600,  'Suspensión y dirección', true),
  ('B', '01', '1', 400,  'Componentes eléctricos ESD', true)
) AS u(pasillo, estante, nivel, capacidad, descripcion, activo)
WHERE NOT EXISTS (
  SELECT 1 FROM ubicaciones x
  WHERE x.pasillo = u.pasillo AND x.estante = u.estante AND COALESCE(x.nivel, '') = COALESCE(u.nivel, '')
);

-- [4/10] Clientes externos / B2B
INSERT INTO clientes (nombre, email, telefono, activo, notas) VALUES
  ('Taller Mecánico del Norte SA', 'b2b.taller.norte@macuin.demo', '+525555100001', true, 'Compra recurrente: frenos y suspensión.'),
  ('Refaccionaria Central del Bajío', 'b2b.refacciones.central@macuin.demo', '+524421020304', true, 'Surtido mixto; picos en fin de mes.'),
  ('Transportes y Servicios López', 'b2b.transportes.lopez@macuin.demo', '+525555100003', true, 'Flotilla; consumibles eléctricos.')
ON CONFLICT (email) DO NOTHING;

-- [5/10] Direcciones (una por cliente; evita duplicar si ya existía la pareja cliente+cp)
INSERT INTO direcciones (calle_principal, num_ext, num_int, colonia, municipio, estado, cp, referencias, cliente_id)
SELECT s.calle, s.ext, s.num_int, s.col, s.mun, s.edo, s.cp, s.ref, c.id
FROM clientes c
JOIN (VALUES
  ('b2b.taller.norte@macuin.demo', 'Av. Insurgentes Sur', '2400', NULL::text, 'Del Valle', 'Ciudad de México', 'CDMX', '03100', 'Recepción B2B'),
  ('b2b.refacciones.central@macuin.demo', 'Blvd. López Mateos', '1805', 'B', 'Jardines del Moral', 'León', 'Guanajuato', '37180', 'Andén 2'),
  ('b2b.transportes.lopez@macuin.demo', 'Calzada Ignacio Zaragoza', '422', NULL, '4 Árboles', 'Ciudad de México', 'CDMX', '15730', '9–14 h')
) AS s(email, calle, ext, num_int, col, mun, edo, cp, ref) ON s.email = c.email
WHERE NOT EXISTS (
  SELECT 1 FROM direcciones d WHERE d.cliente_id = c.id AND d.cp = s.cp
);

-- [6/10] Autopartes (10 piezas; precios y familias variadas para gráficas)
INSERT INTO autopartes (sku_codigo, nombre, descripcion, precio_unitario, imagen_url, categoria_id, marca_id)
SELECT v.sku, v.nombre, v.descripcion, v.precio::numeric(12,2), NULL, cat.id, mar.id
FROM (VALUES
  ('MU-FR-001', 'Pastillas de freno cerámicas delanteras', 'Bajo polvo; SUV y pick-up.', 1249.00, 'Frenos', 'TRW'),
  ('MU-FR-002', 'Disco de freno ventilado 280 mm', 'Par delantero recomendado.', 1899.00, 'Frenos', 'Bosch'),
  ('MU-SU-001', 'Amortiguador delantero a gas', 'Con anclaje estándar MacPherson.', 2150.00, 'Suspensión', 'Monroe'),
  ('MU-SU-002', 'Kit bieletas de barra estabilizadora', 'Incluye tornillería.', 489.00, 'Suspensión', 'TRW'),
  ('MU-FI-001', 'Filtro de aceite spin-on', 'Alta retención de partículas.', 189.00, 'Filtros', 'Mann-Filter'),
  ('MU-FI-002', 'Aceite sintético 5W-30 4 L', 'API SP / ILSAC GF-6.', 549.00, 'Filtros', 'Bosch'),
  ('MU-EL-001', 'Bujía de encendido iridium', 'Motor gasolina eficiente.', 159.00, 'Sistema eléctrico', 'NGK'),
  ('MU-EL-002', 'Sensor MAP', 'Presión absoluta multicanal.', 980.00, 'Sistema eléctrico', 'Bosch'),
  ('MU-MO-001', 'Kit de correa de distribución', 'Incluye tensor y polea.', 1450.00, 'Motor', 'Bosch'),
  ('MU-MO-002', 'Termostato 87 °C', 'Sellado OEM equivalente.', 320.00, 'Motor', 'TRW')
) AS v(sku, nombre, descripcion, precio, cat_nom, mar_nom)
JOIN categorias cat ON cat.nombre = v.cat_nom
JOIN marcas mar ON mar.nombre = v.mar_nom
WHERE NOT EXISTS (SELECT 1 FROM autopartes a WHERE a.sku_codigo = v.sku);

-- [7/10] Inventarios (stock por SKU; ubicaciones A01 y B01)
INSERT INTO inventarios (autoparte_id, ubicacion_id, stock_actual, stock_minimo, pasillo, estante, nivel)
SELECT a.id,
  CASE
    WHEN c.nombre IN ('Frenos', 'Suspensión') THEN (SELECT id FROM ubicaciones WHERE pasillo = 'A' AND estante = '01' ORDER BY id LIMIT 1)
    WHEN c.nombre = 'Sistema eléctrico' THEN (SELECT id FROM ubicaciones WHERE pasillo = 'B' AND estante = '01' ORDER BY id LIMIT 1)
    ELSE (SELECT id FROM ubicaciones WHERE pasillo = 'A' AND estante = '02' ORDER BY id LIMIT 1)
  END,
  v.stk, v.minimo, 'A', '01', '1'
FROM (VALUES
  ('MU-FR-001', 42, 8),
  ('MU-FR-002', 18, 4),
  ('MU-SU-001', 24, 6),
  ('MU-SU-002', 60, 10),
  ('MU-FI-001', 200, 40),
  ('MU-FI-002', 88, 20),
  ('MU-EL-001', 350, 50),
  ('MU-EL-002', 55, 10),
  ('MU-MO-001', 30, 5),
  ('MU-MO-002', 0, 5)
) AS v(sku, stk, minimo)
JOIN autopartes a ON a.sku_codigo = v.sku
JOIN categorias c ON c.id = a.categoria_id
WHERE NOT EXISTS (SELECT 1 FROM inventarios i WHERE i.autoparte_id = a.id);

-- [8/10] Pedidos demo (totales y fechas dispersas para tendencias; usuario interno = ventas)
INSERT INTO pedidos (folio, usuario_id, estatus_id, total, direccion_envio_id, cliente_id, fecha_pedido)
SELECT v.folio,
  (SELECT id FROM usuarios WHERE email = 'ventas@macuin.com' ORDER BY id LIMIT 1),
  (SELECT id FROM estatus_pedido WHERE nombre = v.est ORDER BY id LIMIT 1),
  v.total::numeric(15,2),
  (SELECT d.id FROM direcciones d JOIN clientes c ON c.id = d.cliente_id WHERE c.email = v.cli_email ORDER BY d.id LIMIT 1),
  (SELECT id FROM clientes WHERE email = v.cli_email ORDER BY id LIMIT 1),
  v.fecha::timestamptz
FROM (VALUES
  -- Totales = suma de líneas en [9/10] (reportes coherentes)
  ('DEMO-2026-001', 'Entregado',  3948.00, 'b2b.taller.norte@macuin.demo', '2026-01-14 11:00:00+00'),
  ('DEMO-2026-002', 'Enviado',    2535.00, 'b2b.refacciones.central@macuin.demo', '2026-02-03 15:30:00+00'),
  ('DEMO-2026-003', 'Confirmado', 4825.00, 'b2b.transportes.lopez@macuin.demo', '2026-02-22 09:15:00+00'),
  ('DEMO-2026-004', 'Pendiente',   980.00, 'b2b.taller.norte@macuin.demo', '2026-04-01 13:45:00+00')
) AS v(folio, est, total, cli_email, fecha)
WHERE EXISTS (SELECT 1 FROM usuarios WHERE email = 'ventas@macuin.com')
  AND NOT EXISTS (SELECT 1 FROM pedidos p WHERE p.folio = v.folio);

-- [9/10] Detalles de pedido (líneas que cuadran con totales aproximados + catálogo)
INSERT INTO detalles_pedidos (pedido_id, autoparte_id, cantidad, precio_historico)
SELECT p.id, a.id, l.cant, l.precio::numeric(12,2)
FROM (VALUES
  ('DEMO-2026-001', 'MU-FR-001', 1, 1249.00),
  ('DEMO-2026-001', 'MU-SU-001', 1, 2150.00),
  ('DEMO-2026-001', 'MU-FI-002',  1, 549.00),
  ('DEMO-2026-002', 'MU-FR-002', 1, 1899.00),
  ('DEMO-2026-002', 'MU-EL-001', 4, 159.00),
  ('DEMO-2026-003', 'MU-MO-001', 2, 1450.00),
  ('DEMO-2026-003', 'MU-EL-002', 1, 980.00),
  ('DEMO-2026-003', 'MU-FI-001', 5, 189.00),
  ('DEMO-2026-004', 'MU-EL-002', 1, 980.00)
) AS l(folio, sku, cant, precio)
JOIN pedidos p ON p.folio = l.folio
JOIN autopartes a ON a.sku_codigo = l.sku
WHERE NOT EXISTS (
  SELECT 1 FROM detalles_pedidos dp WHERE dp.pedido_id = p.id AND dp.autoparte_id = a.id
);

-- [10/10] Pagos asociados (montos alineados a pedidos; estados para reportes de cobranza)
INSERT INTO pagos (pedido_id, carrito_id, monto, moneda, estado, pasarela, referencia_externa, respuesta_proveedor)
SELECT p.id, NULL, p.total, 'MXN', v.estado, 'Pasarela demo Macuin', v.ref, v.detalle
FROM pedidos p
JOIN (VALUES
  ('DEMO-2026-001', 'aprobado', 'PAY-DEMO-001', '{"simulado":true,"resultado":"aprobado"}'),
  ('DEMO-2026-002', 'aprobado', 'PAY-DEMO-002', '{"simulado":true,"resultado":"aprobado"}'),
  ('DEMO-2026-003', 'capturado', 'PAY-DEMO-003', '{"simulado":true,"resultado":"capturado"}'),
  ('DEMO-2026-004', 'pendiente', NULL::text, NULL::text)
) AS v(folio, estado, ref, detalle)
ON p.folio = v.folio
WHERE NOT EXISTS (SELECT 1 FROM pagos pg WHERE pg.pedido_id = p.id);

COMMIT;
