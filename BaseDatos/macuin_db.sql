CREATE DATABASE IF NOT EXISTS macuin_db;
USE macuin_db;

-- Una sola tabla para evitar varios JOINS
CREATE TABLE direcciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    calle_principal VARCHAR(150) NOT NULL,
    num_ext VARCHAR(10) NOT NULL,
    num_int VARCHAR(10),
    colonia VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    cp VARCHAR(10) NOT NULL,
    referencias TEXT,
    INDEX idx_cp (cp)
);

-- 2. USUARIOS Y SEGURIDAD
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    rol_id INT NOT NULL,
    direccion_id INT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_rol FOREIGN KEY (rol_id) REFERENCES roles(id),
    CONSTRAINT fk_user_dir FOREIGN KEY (direccion_id) REFERENCES direcciones(id),
    INDEX idx_email (email)
);

-- 3. CATÁLOGO Y ALMACÉN
CREATE TABLE categorias (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) UNIQUE);
CREATE TABLE marcas (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) UNIQUE);

CREATE TABLE autopartes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku_codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio_unitario DECIMAL(12,2) NOT NULL,
    imagen_url VARCHAR(255), --imagenes
    categoria_id INT NOT NULL,
    marca_id INT NOT NULL,
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_auto_cat FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    CONSTRAINT fk_auto_marca FOREIGN KEY (marca_id) REFERENCES marcas(id),
    INDEX idx_sku (sku_codigo)
);

CREATE TABLE inventarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    autoparte_id INT NOT NULL UNIQUE,
    stock_actual INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 5,
    pasillo VARCHAR(10),
    estante VARCHAR(10),
    nivel VARCHAR(10),
    CONSTRAINT fk_inv_auto FOREIGN KEY (autoparte_id) REFERENCES autopartes(id)
);

-- 4. VENTAS Y PEDIDOS
CREATE TABLE estatus_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    folio VARCHAR(20) UNIQUE,
    usuario_id INT NOT NULL,
    estatus_id INT NOT NULL,
    total DECIMAL(15,2) DEFAULT 0.00,
    direccion_envio_id INT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_ped_user FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    CONSTRAINT fk_ped_estatus FOREIGN KEY (estatus_id) REFERENCES estatus_pedido(id),
    CONSTRAINT fk_ped_dir FOREIGN KEY (direccion_envio_id) REFERENCES direcciones(id)
);

CREATE TABLE detalles_pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    autoparte_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_historico DECIMAL(12,2) NOT NULL, --Mantiene el precio al momento del pedido
    subtotal DECIMAL(12,2) AS (cantidad * precio_historico) STORED,
    CONSTRAINT fk_det_ped FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    CONSTRAINT fk_det_auto FOREIGN KEY (autoparte_id) REFERENCES autopartes(id)
);

-- Inserciones Base
INSERT INTO roles (nombre_rol) VALUES ('ADMIN'), ('ALMACEN'), ('CLIENTE');
INSERT INTO estatus_pedido (nombre) VALUES ('PENDIENTE'), ('PAGADO'), ('SURTIENDO'), ('ENVIADO'), ('CANCELADO');