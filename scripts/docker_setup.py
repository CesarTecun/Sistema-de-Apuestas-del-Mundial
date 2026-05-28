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
            print("PostgreSQL está listo")
            return True
        except psycopg2.OperationalError:
            print(f"   Intento {i+1}/{max_retries}...")
            time.sleep(retry_delay)
    
    print("Error: se agotó el tiempo de espera para PostgreSQL")
    return False

def setup_django_environment():
    """Configurar entorno Django para Docker"""
    print("Configurando entorno Django...")
    
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
    print("Entorno Django configurado")

def verify_database_schema():
    """Verificar conexión a la base de datos"""
    print("Verificando conexión a base de datos...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Conexión a base de datos confirmada")
            return True
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return False

def apply_migrations():
    """Aplicar migraciones de Django"""
    print("Aplicando migraciones de Django...")
    
    try:
        # Aplicar migraciones
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("Migraciones aplicadas correctamente")
        return True
        
    except Exception as e:
        print(f"Error aplicando migraciones: {e}")
        return False

def create_superuser():
    """Crear superusuario si no existe"""
    print("Verificando superusuario...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@mundial.com',
                password='admin123'
            )
            print("Superusuario creado (admin/admin123)")
        else:
            print("Superusuario ya existe")
        
        return True
        
    except Exception as e:
        print(f"Error creando o verificando superusuario: {e}")
        return False

def main():
    """Función principal"""
    print("Configurando Django con Docker...")
    print("=" * 60)
    
    # 1. Esperar a PostgreSQL
    if not wait_for_postgres():
        print("No se pudo conectar a PostgreSQL")
        return False
    
    # 2. Configurar Django
    setup_django_environment()
    
    # 3. Verificar conexión a BD
    if not verify_database_schema():
        print("No se pudo conectar a la base de datos")
        return False
    
    # 4. Aplicar migraciones
    if not apply_migrations():
        return False
    
    # 5. Crear superusuario
    if not create_superuser():
        return False
    
    print("\n" + "=" * 60)
    print("Configuración Docker completada")
    print("\nResumen:")
    print("   - PostgreSQL listo")
    print("   - Base de datos lista")
    print("   - Migraciones aplicadas")
    print("   - Superusuario creado")
    print("\nAhora puedes ejecutar:")
    print("   python manage.py runserver")
    print("\nAcceso a la aplicación:")
    print("   Frontend: http://localhost:3000")
    print("   Admin: http://localhost:8000/admin (admin/admin123)")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
