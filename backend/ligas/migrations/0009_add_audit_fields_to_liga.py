# Generated migration for audit fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ligas', '0008_crear_liga_mundial_y_asociar_partidos'),
    ]

    operations = [
        migrations.AddField(
            model_name='liga',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='liga',
            name='updated_by',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='liga',
            name='deleted_by',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='participanteliga',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='participanteliga',
            name='updated_by',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='participanteliga',
            name='deleted_by',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
