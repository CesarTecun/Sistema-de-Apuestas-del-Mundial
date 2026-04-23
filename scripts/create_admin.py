#!/usr/bin/env python
"""
Script para crear un usuario admin en la base de datos.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from backend.usuarios.models import Usuario
from django.contrib.auth.hashers import make_password

def create_admin_user():
    """Crea un usuario admin si no existe"""
    email = "admin@quiniela.com"
    password = "123admin"
    
    try:
        # Verificar si el usuario ya existe
        if Usuario.objects.filter(email=email).exists():
            print(f"El usuario {email} ya existe.")
            return
        
        # Crear el usuario
        usuario = Usuario(
            email=email,
            primer_nombre="Admin",
            primer_apellido="Sistema",
            contrasena=make_password(password),
            fk_rol=1,  # Rol de administrador
            status=True
        )
        usuario.save()
        
        print(f"✅ Usuario admin creado exitosamente:")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
        
    except Exception as e:
        print(f"❌ Error al crear usuario admin: {e}")

if __name__ == '__main__':
    create_admin_user()
