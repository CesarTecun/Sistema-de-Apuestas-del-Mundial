from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0012_partido_fk_partido_origen_local_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                TRUNCATE TABLE jugador RESTART IDENTITY CASCADE;
                TRUNCATE TABLE partido RESTART IDENTITY CASCADE;
                TRUNCATE TABLE seleccion RESTART IDENTITY CASCADE;
            """,
            reverse_sql="""
                -- No se puede deshacer un TRUNCATE de forma trivial
            """,
        ),
    ]
