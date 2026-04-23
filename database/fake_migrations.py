#!/usr/bin/env python
"""
Script para marcar migraciones como aplicadas sin ejecutarlas.
Ejecutar después de crear la base de datos con las tablas manuales.
"""

import os
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
django.setup()

from django.db import connection

# Lista de migraciones a marcar como aplicadas
migrations = [
    ('contenttypes', '0001_initial'),
    ('contenttypes', '0002_remove_content_type_name'),
    ('auth', '0001_initial'),
    ('auth', '0002_alter_permission_name_max_length'),
    ('auth', '0003_alter_user_email_max_length'),
    ('auth', '0004_alter_user_username_opts'),
    ('auth', '0005_alter_user_last_login_null'),
    ('auth', '0006_require_contenttypes_0002'),
    ('auth', '0007_alter_validators_add_error_messages'),
    ('auth', '0008_alter_user_username_max_length'),
    ('auth', '0009_alter_user_last_name_max_length'),
    ('auth', '0010_alter_group_name_max_length'),
    ('auth', '0011_update_proxy_permissions'),
    ('auth', '0012_alter_user_first_name_max_length'),
    ('admin', '0001_initial'),
    ('admin', '0002_logentry_remove_auto_add'),
    ('admin', '0003_logentry_add_action_flag_choices'),
    ('sessions', '0001_initial'),
    ('usuarios', '0001_initial'),
]

if __name__ == '__main__':
    with connection.cursor() as cursor:
        # Verificar si existe la tabla
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'django_migrations'
            );
        """)
        exists = cursor.fetchone()[0]
        
        if not exists:
            print("❌ La tabla django_migrations no existe. Ejecuta primero el init-django-tables.sql")
            sys.exit(1)
        
        print("✅ Marcando migraciones como aplicadas...")
        
        for app, name in migrations:
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied)
                VALUES (%s, %s, NOW())
                ON CONFLICT (app, name) DO NOTHING;
            """, [app, name])
            print(f"  - {app}.{name}")
        
        print(f"\n✅ {len(migrations)} migraciones marcadas como aplicadas")
        print("\nAhora puedes ejecutar el servidor Django:")
        print("  python manage.py runserver")
