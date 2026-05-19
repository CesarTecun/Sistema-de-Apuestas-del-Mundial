from django.db import migrations


def seed_selecciones(apps, schema_editor):
    """Inserta las selecciones participantes del Mundial 2026."""
    Seleccion = apps.get_model('partidos', 'Seleccion')
    paises = [
        'Canadá', 'México', 'Estados Unidos', 'Curazao', 'Haití', 'Panamá',
        'Argentina', 'Brasil', 'Colombia', 'Ecuador', 'Paraguay', 'Uruguay',
        'Austria', 'Bélgica', 'Bosnia y Herzegovina', 'Croacia', 'Chequia',
        'Inglaterra', 'Francia', 'Alemania', 'Países Bajos', 'Noruega',
        'Portugal', 'Escocia', 'España', 'Suecia', 'Suiza', 'Turquía',
        'Australia', 'Irak', 'Irán', 'Japón', 'Jordania', 'Corea del Sur',
        'Catar', 'Arabia Saudita', 'Uzbekistán', 'Nueva Zelanda',
    ]
    for nombre in paises:
        Seleccion.objects.get_or_create(pais=nombre)


def reverse_seed(apps, schema_editor):
    """Elimina las selecciones insertadas (rollback)."""
    Seleccion = apps.get_model('partidos', 'Seleccion')
    paises = [
        'Canadá', 'México', 'Estados Unidos', 'Curazao', 'Haití', 'Panamá',
        'Argentina', 'Brasil', 'Colombia', 'Ecuador', 'Paraguay', 'Uruguay',
        'Austria', 'Bélgica', 'Bosnia y Herzegovina', 'Croacia', 'Chequia',
        'Inglaterra', 'Francia', 'Alemania', 'Países Bajos', 'Noruega',
        'Portugal', 'Escocia', 'España', 'Suecia', 'Suiza', 'Turquía',
        'Australia', 'Irak', 'Irán', 'Japón', 'Jordania', 'Corea del Sur',
        'Catar', 'Arabia Saudita', 'Uzbekistán', 'Nueva Zelanda',
    ]
    Seleccion.objects.filter(pais__in=paises).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_selecciones, reverse_seed),
    ]
