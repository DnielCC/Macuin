## ALMACÉN

# Configuración para el API 
1. se hizo el cambio en el archivo yml, en la parte de flask, en especifico environment, }
    solo se le agrego:
    - API_BASE_URL=http://api:8000 

2. se creo un archivo .env en donde se coloca solamemte:
    API_BASE_URL=http://macuin_api:8000

# Cambios en la API
en la carpeta de router faltaba lo de estatus_pedido, asi que lo agregue,
al igual que en main

# ROUTER
modifique casi todo este archivo en flask, para que funcionara lo de almacén

# requeriments
agregue: requests

# Inserts para la BD
Inserts por si no tiene datos en la base :)

NOTA: SE DEBEN EJECUTAR EN ESTE ORDEN POR LAS FK Y EN TERMINAL GIT BASH

1. Estatus
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO estatus_pedido (nombre) VALUES 
    ('Pendiente'), ('Surtiendo'), ('Empacado'), ('Enviado'), ('Entregado'), ('Cancelado')
    ON CONFLICT DO NOTHING;
    "
2. Roles
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO roles (nombre_rol) VALUES
    ('Administrador'), ('Ventas'), ('Logística'), ('Almacén')
    ON CONFLICT DO NOTHING;
    "
3. Direcciones
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO direcciones (calle_principal, num_ext, num_int, colonia, municipio, estado, cp, referencias) VALUES
    ('Av. Insurgentes Sur', '1234', '5A', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', 'Entre Eugenia y Filadelfia'),
    ('Calle Reforma', '567', NULL, 'Centro', 'Querétaro', 'Querétaro', '76000', 'Frente al parque'),
    ('Blvd. Díaz Ordaz', '890', '2B', 'Milenio III', 'Querétaro', 'Querétaro', '76060', 'Junto a plaza comercial'),
    ('Calle Hidalgo', '321', NULL, 'Centro Histórico', 'San Juan del Río', 'Querétaro', '76800', 'A una cuadra del mercado'),
    ('Av. Tecnológico', '445', '10', 'Lomas', 'Querétaro', 'Querétaro', '76150', 'Edificio azul')
    ON CONFLICT DO NOTHING;
    "
4. Usuarios
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO usuarios (nombre, apellidos, email, password_hash, telefono, rol_id, direccion_id, activo) VALUES
    ('Frank', 'Contreras López', 'admin@macuin.com', 'admin123', '4421001001', 1, 1, TRUE),
    ('María', 'González Ruiz', 'ventas@macuin.com', 'ventas123', '4421002002', 2, 2, TRUE),
    ('Ana', 'Martínez Torres', 'logistica@macuin.com', 'logistica123', '4421003003', 3, 3, TRUE),
    ('Carlos', 'López Hernández', 'almacen@macuin.com', 'almacen123', '4421004004', 4, 4, TRUE),
    ('Roberto', 'Sánchez Pérez', 'cliente1@gmail.com', 'pass1234', '4421005005', 2, 5, TRUE)
    ON CONFLICT DO NOTHING;
    "
5. Categorias
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO categorias (nombre) VALUES
    ('Frenos'), ('Suspensión'), ('Motor'), ('Electricidad'), ('Lubricantes')
    ON CONFLICT DO NOTHING;
    "
6. Marcas
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO marcas (nombre) VALUES
    ('Bosch'), ('Monroe'), ('Denso'), ('ACDelco'), ('Mobil')
    ON CONFLICT DO NOTHING;
    "
7. Autopartes
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO autopartes (sku_codigo, nombre, descripcion, precio_unitario, categoria_id, marca_id) VALUES
    ('FRE-001', 'Disco de Freno Delantero', 'Disco ventilado para eje delantero. Diámetro 280mm.', 850.00, 1, 1),
    ('FRE-009', 'Pastilla de Freno (juego)', 'Juego de 4 pastillas. Cambiar en pares por eje.', 320.00, 1, 1),
    ('SUS-014', 'Amortiguador Trasero', 'Amortiguador de gas. Almacenamiento vertical obligatorio.', 1200.00, 2, 2),
    ('SUS-007', 'Rótula de Dirección', 'Aplicar grasa al montar. Torque máx 120 Nm.', 450.00, 2, 2),
    ('MOT-088', 'Filtro de Aceite', 'Rosca M20x1.5. Compatible con aceite mineral y sintético.', 95.00, 3, 3),
    ('MOT-032', 'Bujía de Encendido', 'Iridio. Espacio entre electrodos: 1.1mm.', 180.00, 3, 3),
    ('ELE-005', 'Batería 12V 60Ah', 'No invertir polaridad. Almacenar en área ventilada.', 1850.00, 4, 4),
    ('LUB-021', 'Aceite Motor 5W-30 (1L)', 'Sintético. Rotación FIFO obligatoria.', 120.00, 5, 5)
    ON CONFLICT DO NOTHING;
    "
8. Investarios
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO inventarios (autoparte_id, stock_actual, stock_minimo, pasillo, estante, nivel) VALUES
    (1, 48, 10, 'A', '01', '1'),
    (2, 124, 20, 'A', '01', '2'),
    (3, 31, 8, 'A', '02', '1'),
    (4, 22, 5, 'A', '02', '2'),
    (5, 210, 30, 'B', '01', '1'),
    (6, 88, 15, 'B', '02', '1'),
    (7, 4, 10, 'C', '01', '1'),
    (8, 73, 20, 'B', '01', '2')
    ON CONFLICT DO NOTHING;
    "
9. Pedidos
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO pedidos (folio, usuario_id, estatus_id, total, direccion_envio_id, fecha_pedido) VALUES
    ('ORD-2401', 5, 1, 1700.00, 5, NOW() - INTERVAL '1 day'),
    ('ORD-2402', 5, 2, 850.00, 5, NOW() - INTERVAL '2 days'),
    ('ORD-2403', 5, 3, 3200.00, 2, NOW() - INTERVAL '3 days'),
    ('ORD-2404', 5, 4, 450.00, 3, NOW() - INTERVAL '10 days'),
    ('ORD-2405', 5, 5, 1200.00, 4, NOW() - INTERVAL '15 days'),
    ('ORD-2406', 5, 1, 640.00, 5, NOW() - INTERVAL '20 days'),
    ('ORD-2407', 5, 2, 1850.00, 2, NOW() - INTERVAL '25 days')
    ON CONFLICT DO NOTHING;
    "
10. detalles_pedidos
    docker exec macuin_db psql -U macuin -d DB_macuin -c "
    INSERT INTO detalles_pedidos (pedido_id, autoparte_id, cantidad, precio_historico) VALUES
    (1, 1, 2, 850.00),
    (2, 1, 1, 850.00),
    (3, 3, 2, 1200.00),
    (3, 5, 5, 95.00),
    (4, 4, 1, 450.00),
    (5, 3, 1, 1200.00),
    (6, 2, 2, 320.00),
    (7, 7, 1, 1850.00)
    ON CONFLICT DO NOTHING;
    "

## ADMINISTRADOR

# Cambios en la API
en la carpeta de router agregue detalles_pedido
al igual que en main, para graficas 

# HTML 
solo agregue una interfaz nueva para los reportes admin_reportes 
(por el momento no esta en mis commits por que aun la estoy trabajando),
agregue una nueva ruta en base.html para reportes

# BD
coloque un rol para los clientes "Cliente"

