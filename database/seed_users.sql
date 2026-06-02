-- ============================================================
-- Seed de usuarios y roles para PostgreSQL (Neon / Render)
-- ============================================================
-- Ejecutar en la consola SQL de Neon o con psql:
--   psql <DATABASE_URL> -f database/seed_users.sql
--
-- Notas:
-- - Las contraseñas están hasheadas con bcrypt_sha256 (Django).
-- - Si ya existen los usuarios, se actualizan sus contraseñas
--   y roles mediante ON CONFLICT.
-- ============================================================

-- 1. Roles base
INSERT INTO rol_usuario (id_rol, descripcion) VALUES
    (1, 'Administrador'),
    (2, 'Usuario')
ON CONFLICT (id_rol) DO UPDATE SET descripcion = EXCLUDED.descripcion;

-- 2. Usuarios base
-- adminquiniela / admin123  (rol 1 = Admin elevado)
-- user / user123            (rol 2 = Usuario estándar)
-- admindb / admin123        (rol 1 = Admin DB)

INSERT INTO usuario (
    primer_nombre,
    primer_apellido,
    email,
    contrasena,
    fk_rol,
    status,
    email_verificado,
    deleted_at
) VALUES
    (
        'Admin',
        'Quiniela',
        'adminquiniela@mundial.com',
        'bcrypt_sha256$$2b$12$rCkPIRGtZfY6WfqN9VfA7eGXGo5U7AAcxlEWQiTzl/tUE16GMh5Mm',
        1,
        true,
        false,
        NULL
    ),
    (
        'Usuario',
        'Estandar',
        'user@mundial.com',
        'bcrypt_sha256$$2b$12$REhjdipnCYScpXx0kPas0.b7xpsWff.QAey4gaH.wNVIZlfzA/DHC',
        2,
        true,
        false,
        NULL
    ),
    (
        'Admin',
        'DB',
        'admindb@mundial.com',
        'bcrypt_sha256$$2b$12$rCkPIRGtZfY6WfqN9VfA7eGXGo5U7AAcxlEWQiTzl/tUE16GMh5Mm',
        1,
        true,
        false,
        NULL
    )
ON CONFLICT (email) DO UPDATE SET
    contrasena = EXCLUDED.contrasena,
    fk_rol = EXCLUDED.fk_rol,
    status = EXCLUDED.status,
    deleted_at = EXCLUDED.deleted_at;
