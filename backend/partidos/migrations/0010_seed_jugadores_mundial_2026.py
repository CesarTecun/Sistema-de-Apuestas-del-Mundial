from django.db import migrations

def parse_nombre(nombre):
    partes = nombre.split()
    if len(partes) == 1:
        return partes[0], None, None, None
    elif len(partes) == 2:
        return partes[0], None, partes[1], None
    elif len(partes) == 3:
        return partes[0], partes[1], partes[2], None
    elif len(partes) >= 4:
        return partes[0], partes[1], partes[2], ' '.join(partes[3:])
    return None, None, None, None

def seed_jugadores(apps, schema_editor):
    Seleccion = apps.get_model('partidos', 'Seleccion')
    Jugador = apps.get_model('partidos', 'Jugador')
    from backend.partidos.jugadores_mundial_2026_data import JUGADORES_DATA, SELECCIONES_FALTANTES, PAIS_TO_ID_EXISTENTE

    # 1. Ajustar la secuencia de seleccion al MAX(id) para evitar conflictos en DB nueva
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id_seleccion) FROM seleccion")
    max_id = cursor.fetchone()[0] or 0
    cursor.execute(
        "SELECT setval(pg_get_serial_sequence('seleccion', 'id_seleccion'), %s, true)",
        [max_id]
    )

    pais_to_id = dict(PAIS_TO_ID_EXISTENTE)

    # 2. Crear selecciones faltantes con get_or_create (ahora la secuencia está bien)
    for pais in SELECCIONES_FALTANTES:
        sel, created = Seleccion.objects.get_or_create(
            pais=pais,
            defaults={'status': True, 'deleted_at': None}
        )
        pais_to_id[pais] = sel.id_seleccion

    # 3. Insertar jugadores por bulk_create
    jugadores_objs = []
    for pais, dorsal, nombre, posicion in JUGADORES_DATA:
        fk_id = pais_to_id.get(pais)
        if not fk_id:
            print(f"WARN: No se encontró selección para {pais}")
            continue
        pn, sn, pa, sa = parse_nombre(nombre)
        jugadores_objs.append(Jugador(
            primer_nombre=pn,
            segundo_nombre=sn,
            primer_apellido=pa,
            segundo_apellido=sa,
            dorsal=dorsal,
            posicion=posicion,
            fk_id_seleccion=fk_id,
            status=True
        ))

    if jugadores_objs:
        Jugador.objects.bulk_create(jugadores_objs, batch_size=500)
        print(f"Insertados {len(jugadores_objs)} jugadores.")

def reverse_seed(apps, schema_editor):
    Jugador = apps.get_model('partidos', 'Jugador')
    from backend.partidos.jugadores_mundial_2026_data import JUGADORES_DATA, PAIS_TO_ID_EXISTENTE, SELECCIONES_FALTANTES
    # Reconstruir mapeo pais -> fk_id para eliminar exacto
    pais_to_id = dict(PAIS_TO_ID_EXISTENTE)
    Seleccion = apps.get_model('partidos', 'Seleccion')
    for pais in SELECCIONES_FALTANTES:
        try:
            sel = Seleccion.objects.get(pais=pais)
            pais_to_id[pais] = sel.id_seleccion
        except Seleccion.DoesNotExist:
            pass
    for pais, dorsal, nombre, posicion in JUGADORES_DATA:
        fk_id = pais_to_id.get(pais)
        if fk_id:
            Jugador.objects.filter(fk_id_seleccion=fk_id, dorsal=dorsal).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('partidos', '0009_seed_partidos_mundial_2026'),
    ]

    operations = [
        migrations.RunPython(seed_jugadores, reverse_seed),
    ]
