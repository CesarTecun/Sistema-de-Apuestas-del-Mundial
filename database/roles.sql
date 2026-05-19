-- ============================================================
-- Roles de Base de Datos PostgreSQL
-- ============================================================
-- Ejecutar manualmente como superusuario (postgres):
--   psql -U postgres -d quiniela -f database/roles.sql
--
-- Requisito: separación de roles con permisos mínimos.
-- El rol de aplicación NO debe tener permisos DDL.
-- ============================================================

-- 1. Rol de aplicación (backend Django) — permisos DML únicamente
CREATE ROLE quiniela_app WITH LOGIN PASSWORD 'CAMBIAR_PASSWORD_APP' NOSUPERUSER NOCREATEDB NOCREATEROLE;

-- 2. Rol de solo lectura (reportes / dashboards) — SELECT únicamente
CREATE ROLE quiniela_readonly WITH LOGIN PASSWORD 'CAMBIAR_PASSWORD_READONLY' NOSUPERUSER NOCREATEDB NOCREATEROLE;

-- 3. Conectar a la base de datos
GRANT CONNECT ON DATABASE quiniela TO quiniela_app;
GRANT CONNECT ON DATABASE quiniela TO quiniela_readonly;

-- 4. Uso del schema public
GRANT USAGE ON SCHEMA public TO quiniela_app;
GRANT USAGE ON SCHEMA public TO quiniela_readonly;

-- 5. Permisos sobre tablas (DML para app, SELECT para readonly)
-- Se aplica a tablas existentes y futuras mediante DEFAULT PRIVILEGES
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO quiniela_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO quiniela_readonly;

-- Para tablas ya creadas (si se ejecuta después de migrate)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO quiniela_app;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO quiniela_readonly;

-- 6. Permisos sobre secuencias (necesario para INSERT con campos SERIAL)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO quiniela_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO quiniela_app;

-- 7. Revocar permisos DDL implícitos (CREATE, DROP, ALTER, etc.)
-- Los roles ya se crearon sin CREATEDB ni CREATEROLE, pero reforzamos:
REVOKE CREATE ON SCHEMA public FROM quiniela_app;
REVOKE CREATE ON SCHEMA public FROM quiniela_readonly;

-- ============================================================
-- Uso en .env
-- ============================================================
-- Para el backend:
--   DB_USER=quiniela_app
--   DB_PASSWORD=CAMBIAR_PASSWORD_APP
--
-- Para herramientas de reporting (opcional):
--   DB_USER=quiniela_readonly
--   DB_PASSWORD=CAMBIAR_PASSWORD_READONLY
-- ============================================================
