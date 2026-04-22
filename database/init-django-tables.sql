-- =====================================================
-- Script de inicialización de tablas Django
-- Se ejecuta automáticamente al crear el contenedor
-- =====================================================

-- Tabla django_migrations (control de migraciones)
CREATE TABLE IF NOT EXISTS django_migrations (
    id serial PRIMARY KEY,
    app varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);

-- Tabla django_content_type
CREATE TABLE IF NOT EXISTS django_content_type (
    id serial PRIMARY KEY,
    app_label varchar(100) NOT NULL,
    model varchar(100) NOT NULL,
    CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model)
);

-- Tabla django_session
CREATE TABLE IF NOT EXISTS django_session (
    session_key varchar(40) NOT NULL PRIMARY KEY,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
CREATE INDEX IF NOT EXISTS django_session_expire_date_a5c62663 ON django_session (expire_date);
CREATE INDEX IF NOT EXISTS django_session_session_key_c0390e0f_like ON django_session (session_key varchar_pattern_ops);

-- Tabla django_admin_log
CREATE TABLE IF NOT EXISTS django_admin_log (
    id serial PRIMARY KEY,
    action_time timestamp with time zone NOT NULL,
    user_id integer,
    content_type_id integer,
    object_id text,
    object_repr varchar(200) NOT NULL,
    action_flag smallint NOT NULL CONSTRAINT django_admin_log_action_flag_check CHECK (action_flag >= 0),
    change_message text NOT NULL
);

-- Tablas de autenticación (auth)
CREATE TABLE IF NOT EXISTS auth_permission (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename varchar(100) NOT NULL,
    CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename)
);

CREATE TABLE IF NOT EXISTS auth_group (
    id serial PRIMARY KEY,
    name varchar(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id bigserial PRIMARY KEY,
    group_id integer NOT NULL,
    permission_id integer NOT NULL,
    CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id)
);

-- Insertar content types básicos de Django
INSERT INTO django_content_type (app_label, model) VALUES
    ('admin', 'logentry'),
    ('auth', 'permission'),
    ('auth', 'group'),
    ('contenttypes', 'contenttype'),
    ('sessions', 'session')
ON CONFLICT (app_label, model) DO NOTHING;

-- Marcar migraciones como aplicadas (para que Django no intente recrearlas)
INSERT INTO django_migrations (app, name, applied) VALUES
    ('contenttypes', '0001_initial', NOW()),
    ('contenttypes', '0002_remove_content_type_name', NOW()),
    ('auth', '0001_initial', NOW()),
    ('auth', '0002_alter_permission_name_max_length', NOW()),
    ('auth', '0003_alter_user_email_max_length', NOW()),
    ('auth', '0004_alter_user_username_opts', NOW()),
    ('auth', '0005_alter_user_last_login_null', NOW()),
    ('auth', '0006_require_contenttypes_0002', NOW()),
    ('auth', '0007_alter_validators_add_error_messages', NOW()),
    ('auth', '0008_alter_user_username_max_length', NOW()),
    ('auth', '0009_alter_user_last_name_max_length', NOW()),
    ('auth', '0010_alter_group_name_max_length', NOW()),
    ('auth', '0011_update_proxy_permissions', NOW()),
    ('auth', '0012_alter_user_first_name_max_length', NOW()),
    ('admin', '0001_initial', NOW()),
    ('admin', '0002_logentry_remove_auto_add', NOW()),
    ('admin', '0003_logentry_add_action_flag_choices', NOW()),
    ('sessions', '0001_initial', NOW())
ON CONFLICT (app, name) DO NOTHING;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
