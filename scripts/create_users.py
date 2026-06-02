#!/usr/bin/env python
"""
Script para crear los usuarios base del sistema en la base de datos.
Ejecutar con: python scripts/create_users.py

Requiere que las variables de entorno de la BD estén configuradas
(.env o entorno activo).
"""

import os
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django
django.setup()

from backend.usuarios.models import Usuario, RolUsuario
from django.contrib.auth.hashers import make_password


USERS = [
    {
        'email': 'adminquiniela@mundial.com',
        'password': 'admin123',
        'primer_nombre': 'Admin',
        'primer_apellido': 'Quiniela',
        'fk_rol': 1,
    },
    {
        'email': 'user@mundial.com',
        'password': 'user123',
        'primer_nombre': 'Usuario',
        'primer_apellido': 'Estandar',
        'fk_rol': 2,
    },
    {
        'email': 'admindb@mundial.com',
        'password': 'admin123',
        'primer_nombre': 'Admin',
        'primer_apellido': 'DB',
        'fk_rol': 1,
    },
]

ROLES = [
    {'id_rol': 1, 'descripcion': 'Administrador'},
    {'id_rol': 2, 'descripcion': 'Usuario'},
]


def seed_roles():
    """Crea los roles base si no existen."""
    for rol_data in ROLES:
        rol, created = RolUsuario.objects.get_or_create(
            id_rol=rol_data['id_rol'],
            defaults={'descripcion': rol_data['descripcion']}
        )
        if created:
            print(f"  Rol creado: {rol.descripcion} (id={rol.id_rol})")
        else:
            print(f"  Rol ya existe: {rol.descripcion} (id={rol.id_rol})")


def create_users():
    """Crea los usuarios base del sistema."""
    for user_data in USERS:
        email = user_data['email']
        password = user_data['password']

        usuario, created = Usuario.objects.get_or_create(
            email=email,
            defaults={
                'primer_nombre': user_data['primer_nombre'],
                'primer_apellido': user_data['primer_apellido'],
                'contrasena': make_password(password),
                'fk_rol': user_data['fk_rol'],
                'status': True,
            }
        )

        if created:
            print(f"  Usuario creado: {email} / {password} (rol={user_data['fk_rol']})")
        else:
            # Actualizar contraseña y rol por si cambiaron
            usuario.contrasena = make_password(password)
            usuario.fk_rol = user_data['fk_rol']
            usuario.status = True
            usuario.save(update_fields=['contrasena', 'fk_rol', 'status'])
            print(f"  Usuario actualizado: {email} / {password} (rol={user_data['fk_rol']})")


if __name__ == '__main__':
    print("Creando roles base...")
    seed_roles()
    print("Creando usuarios base...")
    create_users()
    print("Done.")
