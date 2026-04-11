-- Corrige nombres/descripciones si quedaron con "??" por cliente psql o codificación al insertar.
-- Ejecutar: docker exec -i macuin_db psql -U macuin -d DB_macuin < scripts/fix_autopartes_textos_utf8.sql

BEGIN;

UPDATE autopartes SET
  nombre = 'Pastillas de freno cerámicas delanteras',
  descripcion = 'Bajo polvo; SUV y pick-up.'
WHERE sku_codigo = 'MU-FR-001';

UPDATE autopartes SET
  nombre = 'Disco de freno ventilado 280 mm',
  descripcion = 'Par delantero recomendado.'
WHERE sku_codigo = 'MU-FR-002';

UPDATE autopartes SET
  nombre = 'Amortiguador delantero a gas',
  descripcion = 'Con anclaje estándar MacPherson.'
WHERE sku_codigo = 'MU-SU-001';

UPDATE autopartes SET
  nombre = 'Kit bieletas de barra estabilizadora',
  descripcion = 'Incluye tornillería.'
WHERE sku_codigo = 'MU-SU-002';

UPDATE autopartes SET
  nombre = 'Filtro de aceite spin-on',
  descripcion = 'Alta retención de partículas.'
WHERE sku_codigo = 'MU-FI-001';

UPDATE autopartes SET
  nombre = 'Aceite sintético 5W-30 4 L',
  descripcion = 'API SP / ILSAC GF-6.'
WHERE sku_codigo = 'MU-FI-002';

UPDATE autopartes SET
  nombre = 'Bujía de encendido iridium',
  descripcion = 'Motor gasolina eficiente.'
WHERE sku_codigo = 'MU-EL-001';

UPDATE autopartes SET
  nombre = 'Sensor MAP',
  descripcion = 'Presión absoluta multicanal.'
WHERE sku_codigo = 'MU-EL-002';

UPDATE autopartes SET
  nombre = 'Kit de correa de distribución',
  descripcion = 'Incluye tensor y polea.'
WHERE sku_codigo = 'MU-MO-001';

UPDATE autopartes SET
  nombre = 'Termostato 87 °C',
  descripcion = 'Sellado OEM equivalente.'
WHERE sku_codigo = 'MU-MO-002';

COMMIT;
