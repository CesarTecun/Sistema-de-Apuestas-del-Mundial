from django.db import migrations


def seed_sedes(apps, schema_editor):
    """Inserta las sedes del Mundial 2026."""
    Sede = apps.get_model('core', 'Sede')
    sedes = [
        ('Ciudad de México', 'Estadio Azteca'),
        ('Monterrey', 'Estadio BBVA'),
        ('Guadalajara / Zapopan', 'Estadio Akron'),
        ('Vancouver', 'BC Place'),
        ('Toronto', 'BMO Field'),
        ('Nueva York / Nueva Jersey', 'MetLife Stadium'),
        ('Dallas / Arlington', 'AT&T Stadium'),
        ('Atlanta', 'Mercedes-Benz Stadium'),
        ('Los Ángeles / Inglewood', 'SoFi Stadium'),
        ('Miami', 'Hard Rock Stadium'),
        ('Boston / Foxborough', 'Gillette Stadium'),
        ('Houston', 'NRG Stadium'),
        ('Kansas City', 'GEHA Field at Arrowhead Stadium'),
        ('Filadelfia', 'Lincoln Financial Field'),
        ("San Francisco Bay Area / Santa Clara", "Levi's Stadium"),
        ('Seattle', 'Lumen Field'),
    ]
    for ciudad, estadio in sedes:
        Sede.objects.get_or_create(ciudad=ciudad, estadio=estadio)


def reverse_seed(apps, schema_editor):
    """Elimina las sedes insertadas (rollback)."""
    Sede = apps.get_model('core', 'Sede')
    estadios = [
        'Estadio Azteca', 'Estadio BBVA', 'Estadio Akron', 'BC Place',
        'BMO Field', 'MetLife Stadium', 'AT&T Stadium', 'Mercedes-Benz Stadium',
        'SoFi Stadium', 'Hard Rock Stadium', 'Gillette Stadium', 'NRG Stadium',
        'GEHA Field at Arrowhead Stadium', 'Lincoln Financial Field',
        "Levi's Stadium", 'Lumen Field',
    ]
    Sede.objects.filter(estadio__in=estadios).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_sedes, reverse_seed),
    ]
