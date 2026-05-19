from django.db import migrations


def seed_fases(apps, schema_editor):
    """Inserta las fases del Mundial 2026."""
    FaseGrupo = apps.get_model('core', 'FaseGrupo')
    fases = [
        (1, 'Fase de Grupos'),
        (2, 'Octavos de Final'),
        (3, 'Cuartos de Final'),
        (4, 'Semifinales'),
        (5, 'Final'),
        (6, 'Tercer Lugar'),
    ]
    for id_fase, nombre in fases:
        FaseGrupo.objects.get_or_create(id_fase=id_fase, defaults={'nombre_fase': nombre})


def reverse_seed(apps, schema_editor):
    """Elimina las fases insertadas (rollback)."""
    FaseGrupo = apps.get_model('core', 'FaseGrupo')
    nombres = [
        'Fase de Grupos', 'Octavos de Final', 'Cuartos de Final',
        'Semifinales', 'Final', 'Tercer Lugar',
    ]
    FaseGrupo.objects.filter(nombre_fase__in=nombres).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_seed_sedes'),
    ]

    operations = [
        migrations.RunPython(seed_fases, reverse_seed),
    ]
