from django.db import migrations


def seed_banderas(apps, schema_editor):
    """Asigna URLs de banderas a las selecciones usando flagcdn.com."""
    Seleccion = apps.get_model('partidos', 'Seleccion')
    banderas = {
        'Canadá': 'ca',
        'México': 'mx',
        'Estados Unidos': 'us',
        'Curazao': 'cw',
        'Haití': 'ht',
        'Panamá': 'pa',
        'Argentina': 'ar',
        'Brasil': 'br',
        'Colombia': 'co',
        'Ecuador': 'ec',
        'Paraguay': 'py',
        'Uruguay': 'uy',
        'Austria': 'at',
        'Bélgica': 'be',
        'Bosnia y Herzegovina': 'ba',
        'Croacia': 'hr',
        'Chequia': 'cz',
        'Inglaterra': 'gb-eng',
        'Francia': 'fr',
        'Alemania': 'de',
        'Países Bajos': 'nl',
        'Noruega': 'no',
        'Portugal': 'pt',
        'Escocia': 'gb-sct',
        'España': 'es',
        'Suecia': 'se',
        'Suiza': 'ch',
        'Turquía': 'tr',
        'Australia': 'au',
        'Irak': 'iq',
        'Irán': 'ir',
        'Japón': 'jp',
        'Jordania': 'jo',
        'Corea del Sur': 'kr',
        'Catar': 'qa',
        'Arabia Saudita': 'sa',
        'Uzbekistán': 'uz',
        'Nueva Zelanda': 'nz',
    }
    for pais, codigo in banderas.items():
        Seleccion.objects.filter(pais=pais).update(bandera=f'https://flagcdn.com/{codigo}.svg')


def reverse_seed(apps, schema_editor):
    """Quita las URLs de banderas (rollback)."""
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
    Seleccion.objects.filter(pais__in=paises).update(bandera=None)


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0002_seed_selecciones'),
    ]

    operations = [
        migrations.RunPython(seed_banderas, reverse_seed),
    ]
