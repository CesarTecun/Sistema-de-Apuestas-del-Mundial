from django.db import migrations

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('partidos', '0010_seed_jugadores_mundial_2026'),
    ]

    operations = [
        migrations.RunPython(noop, noop),
    ]
