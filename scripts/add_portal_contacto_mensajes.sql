-- Tabla para mensajes de contacto del portal Laravel (API Macuin / panel Flask).
-- Ejecutar si la BD ya existía antes de añadir el modelo (create_all no recrea esquema).
--   docker exec -i macuin_db psql -U macuin -d DB_macuin -v ON_ERROR_STOP=1 -f scripts/add_portal_contacto_mensajes.sql

SET client_encoding TO 'UTF8';

CREATE TABLE IF NOT EXISTS portal_contacto_mensajes (
    id SERIAL PRIMARY KEY,
    laravel_contact_message_id INTEGER,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefono VARCHAR(40),
    asunto VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT false,
    read_at TIMESTAMPTZ,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_portal_contacto_laravel_id UNIQUE (laravel_contact_message_id)
);

CREATE INDEX IF NOT EXISTS ix_portal_contacto_mensajes_email ON portal_contacto_mensajes (email);
CREATE INDEX IF NOT EXISTS ix_portal_contacto_mensajes_creado ON portal_contacto_mensajes (creado_en DESC);
