from django.db import migrations


def seed_codigo_iso(apps, schema_editor):
    """Llena codigo_iso para las selecciones existentes del Mundial 2026."""
    Seleccion = apps.get_model('partidos', 'Seleccion')

    PAIS_A_ISO = {
        'Canadá': 'CAN',
        'México': 'MEX',
        'Estados Unidos': 'USA',
        'Curazao': 'CUW',
        'Haití': 'HTI',
        'Panamá': 'PAN',
        'Argentina': 'ARG',
        'Brasil': 'BRA',
        'Colombia': 'COL',
        'Ecuador': 'ECU',
        'Paraguay': 'PRY',
        'Uruguay': 'URY',
        'Austria': 'AUT',
        'Bélgica': 'BEL',
        'Bosnia y Herzegovina': 'BIH',
        'Croacia': 'HRV',
        'Chequia': 'CZE',
        'Inglaterra': 'ENG',
        'Francia': 'FRA',
        'Alemania': 'DEU',
        'Países Bajos': 'NLD',
        'Noruega': 'NOR',
        'Portugal': 'PRT',
        'Escocia': 'SCO',
        'España': 'ESP',
        'Suecia': 'SWE',
        'Suiza': 'CHE',
        'Turquía': 'TUR',
        'Australia': 'AUS',
        'Irak': 'IRQ',
        'Irán': 'IRN',
        'Japón': 'JPN',
        'Jordania': 'JOR',
        'Corea del Sur': 'KOR',
        'Catar': 'QAT',
        'Arabia Saudita': 'SAU',
        'Uzbekistán': 'UZB',
        'Nueva Zelanda': 'NZL',
    }

    for pais, codigo in PAIS_A_ISO.items():
        seleccion = Seleccion.objects.filter(pais=pais).first()
        if seleccion:
            seleccion.codigo_iso = codigo
            seleccion.save(update_fields=['codigo_iso'])


def reverse_seed_codigo_iso(apps, schema_editor):
    """Elimina los códigos ISO asignados."""
    Seleccion = apps.get_model('partidos', 'Seleccion')
    Seleccion.objects.update(codigo_iso=None)


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0005_add_codigo_iso_seleccion'),
    ]

    operations = [
        migrations.RunPython(seed_codigo_iso, reverse_seed_codigo_iso),
    ]
