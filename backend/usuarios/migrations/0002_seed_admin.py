from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_admin(apps, schema_editor):
    """Crea el usuario administrador por defecto."""
    Usuario = apps.get_model('usuarios', 'Usuario')
    usuario, creado = Usuario.objects.get_or_create(
        email='admin@mundial.com',
        defaults={
            'primer_nombre': 'Admin',
            'primer_apellido': 'Mundial',
            'fk_rol': 1,
            'status': True,
            'contrasena': make_password('admin123'),
        }
    )
    if not creado:
        usuario.contrasena = make_password('admin123')
        usuario.save(update_fields=['contrasena'])


def reverse_seed(apps, schema_editor):
    """Elimina el usuario administrador (rollback)."""
    Usuario = apps.get_model('usuarios', 'Usuario')
    Usuario.objects.filter(email='admin@mundial.com').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_admin, reverse_seed),
    ]
