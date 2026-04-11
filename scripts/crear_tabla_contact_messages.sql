-- Tabla contact_messages (Laravel) si aún no existe (p. ej. sin `php artisan migrate`).
-- Ejecutar contra la misma BD que usa Laravel (Docker: macuin_db).
SET client_encoding TO 'UTF8';

CREATE TABLE IF NOT EXISTS contact_messages (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(40) NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    admin_reply TEXT NULL,
    replied_at TIMESTAMPTZ NULL,
    is_read BOOLEAN NOT NULL DEFAULT false,
    read_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NULL,
    updated_at TIMESTAMPTZ NULL
);

CREATE INDEX IF NOT EXISTS contact_messages_created_at_index ON contact_messages (created_at DESC);
CREATE INDEX IF NOT EXISTS contact_messages_is_read_index ON contact_messages (is_read);

-- Si la tabla ya existía de una migración antigua, añade columnas de respuesta del administrador.
ALTER TABLE contact_messages ADD COLUMN IF NOT EXISTS admin_reply TEXT NULL;
ALTER TABLE contact_messages ADD COLUMN IF NOT EXISTS replied_at TIMESTAMPTZ NULL;
