# Generated manually on 2026-05-25

from django.db import migrations


def crear_liga_mundial_y_asociar_partidos(apps, schema_editor):
    """
    Crea la liga publica 'mundial' y asocia todos los partidos existentes a ella.
    """
    Liga = apps.get_model('ligas', 'Liga')
    PartidoLiga = apps.get_model('ligas', 'PartidoLiga')
    Partido = apps.get_model('partidos', 'Partido')

    # Crear u obtener la liga mundial (idempotente)
    liga_mundial, creada = Liga.objects.update_or_create(
        nombre_liga='mundial',
        defaults={
            'fk_administrador': None,
            'monto_total_recaudado': 0,
            'estado': 'Activa',
            'tipo_liga': 'Diversion',
            'descripcion': 'Liga publica del Mundial 2026 con todos los partidos disponibles.',
            'es_publica': True,
            'cupo_maximo': None,
            'requiere_aprobacion': False,
            'status': True,
        }
    )

    if creada:
        print(f'[Migration] Liga "mundial" creada con id={liga_mundial.id_liga}')
    else:
        print(f'[Migration] Liga "mundial" actualizada/obtenida con id={liga_mundial.id_liga}')

    # Obtener todos los partidos existentes (activos)
    partidos = Partido.objects.filter(status=True)
    total_asociados = 0
    total_existentes = 0

    for partido in partidos:
        _, creado = PartidoLiga.objects.get_or_create(
            fk_id_liga=liga_mundial.id_liga,
            fk_id_partido=partido.id_partido
        )
        if creado:
            total_asociados += 1
        else:
            total_existentes += 1

        # Actualizar fk_id_liga del partido para que apunte a la liga mundial
        if partido.fk_id_liga != liga_mundial.id_liga:
            partido.fk_id_liga = liga_mundial.id_liga
            partido.save(update_fields=['fk_id_liga'])

    print(
        f'[Migration] Partidos asociados a liga mundial: '
        f'{total_asociados} nuevos, {total_existentes} ya existentes, '
        f'{partidos.count()} total en BD'
    )


def revertir_liga_mundial(apps, schema_editor):
    """
    Reversion: elimina la liga "mundial" y sus PartidoLiga asociados.
    """
    Liga = apps.get_model('ligas', 'Liga')
    PartidoLiga = apps.get_model('ligas', 'PartidoLiga')

    liga_mundial = Liga.objects.filter(nombre_liga='mundial').first()
    if liga_mundial:
        PartidoLiga.objects.filter(fk_id_liga=liga_mundial.id_liga).delete()
        liga_mundial.delete()
        print('[Migration] Liga "mundial" y sus asociaciones eliminadas.')


class Migration(migrations.Migration):
    dependencies = [
        ('ligas', '0007_liga_cupo_maximo_liga_descripcion_liga_es_publica_and_more'),
        ('partidos', '0016_seed_jugadores_v2'),
    ]

    operations = [
        migrations.RunPython(
            crear_liga_mundial_y_asociar_partidos,
            revertir_liga_mundial,
        ),
    ]
