#!/usr/bin/env python3
"""
Script de configuración para Docker + Django
Ejecutar después de docker-compose up
"""

import os
import sys
import time
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import connection
import psycopg2

def wait_for_postgres():
    """Esperar a que PostgreSQL esté listo"""
    print("⏳ Esperando a que PostgreSQL esté listo...")
    
    max_retries = 30
    retry_delay = 2
    
    for i in range(max_retries):
        try:
            # Intentar conectar a PostgreSQL
            conn = psycopg2.connect(
                host='localhost',
                port=5432,
                database='quiniela',
                user='postgres',
                password='PASSWORD'
            )
            conn.close()
            print("✅ PostgreSQL está listo")
            return True
        except psycopg2.OperationalError:
            print(f"   Intento {i+1}/{max_retries}...")
            time.sleep(retry_delay)
    
    print("❌ Timeout esperando a PostgreSQL")
    return False

def setup_django_environment():
    """Configurar entorno Django para Docker"""
    print("🔧 Configurando entorno Django...")
    
    # Configurar variables de entorno para Docker
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    # Actualizar configuración de base de datos para Docker
    if 'DATABASES' in settings.__dict__:
        settings.DATABASES['default'] = {
            'NAME': 'quiniela',
            'USER': 'postgres',
            'PASSWORD': 'PASSWORD',
            'HOST': 'localhost',
            'PORT': '5432',
            'ENGINE': 'django.db.backends.postgresql',
        }
    
    django.setup()
    print("✅ Entorno Django configurado")

def verify_database_schema():
    """Verificar que el esquema de la base de datos esté completo"""
    print("🔍 Verificando esquema de base de datos...")
    
    try:
        with connection.cursor() as cursor:
            # Verificar tablas críticas
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = [
                'usuario', 'liga', 'partido', 'seleccion', 'jugador',
                'fase_grupo', 'sede', 'rol_usuario', 'sesion_usuario',
                'equipoliga', 'partido_liga', 'posiciones_torneo',
                'gol', 'historial_ganador', 'ranking', 'premio',
                'pronostico', 'bitacora', 'audit_log'
            ]
            
            missing_tables = [t for t in required_tables if t not in tables]
            
            if missing_tables:
                print(f"❌ Faltan tablas: {missing_tables}")
                print("📝 El init-db.sql debería haberlas creado automáticamente")
                return False
            else:
                print(f"✅ Todas las {len(tables)} tablas encontradas")
                
                # Verificar datos de ejemplo
                cursor.execute("SELECT COUNT(*) FROM seleccion")
                selecciones_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM liga")
                ligas_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM partido")
                partidos_count = cursor.fetchone()[0]
                
                print(f"   📊 Datos: {selecciones_count} selecciones, {ligas_count} ligas, {partidos_count} partidos")
                return True
    
    except Exception as e:
        print(f"❌ Error verificando esquema: {e}")
        return False

def apply_migrations():
    """Aplicar migraciones de Django"""
    print("🔄 Aplicando migraciones de Django...")
    
    try:
        # Verificar columna name en django_content_type
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'django_content_type' AND column_name = 'name'
            """)
            if not cursor.fetchone():
                print("➕ Agregando columna 'name' a django_content_type...")
                cursor.execute("ALTER TABLE django_content_type ADD COLUMN name VARCHAR(100)")
                cursor.execute("UPDATE django_content_type SET name = model")
                print("✅ Columna 'name' agregada")
        
        # Aplicar migraciones
        execute_from_command_line(['manage.py', 'migrate', '--fake-initial'])
        execute_from_command_line(['manage.py', 'migrate', '--fake'])
        
        print("✅ Migraciones aplicadas correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando migraciones: {e}")
        return False

def create_superuser():
    """Crear superusuario si no existe"""
    print("👤 Verificando superusuario...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@mundial.com',
                password='admin123'
            )
            print("✅ Superusuario creado (admin/admin123)")
        else:
            print("✅ Superusuario ya existe")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con superusuario: {e}")
        return False

def main():
    """Función principal"""
    print("🐳 Configurando Django con Docker...")
    print("=" * 60)
    
    # 1. Esperar a PostgreSQL
    if not wait_for_postgres():
        print("❌ No se pudo conectar a PostgreSQL")
        return False
    
    # 2. Configurar Django
    setup_django_environment()
    
    # 3. Verificar esquema
    if not verify_database_schema():
        print("❌ El esquema de la base de datos está incompleto")
        print("📝 Asegúrate que el init-db.sql se ejecutó correctamente en Docker")
        return False
    
    # 4. Aplicar migraciones
    if not apply_migrations():
        return False
    
    # 5. Crear superusuario
    if not create_superuser():
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ¡Configuración Docker completada!")
    print("\n📝 Resumen:")
    print("   ✅ PostgreSQL listo")
    print("   ✅ Esquema de base de datos completo")
    print("   ✅ Migraciones aplicadas")
    print("   ✅ Superusuario creado")
    print("\n🚀 Ahora puedes ejecutar:")
    print("   python manage.py runserver")
    print("\n🌐 Acceso a la aplicación:")
    print("   Frontend: http://localhost:3000")
    print("   Admin: http://localhost:8000/admin (admin/admin123)")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
