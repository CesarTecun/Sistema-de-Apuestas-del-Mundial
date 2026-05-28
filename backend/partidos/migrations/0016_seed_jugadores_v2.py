import ast
import os

from django.db import migrations


def _load_jugadores_data():
    """Carga JUGADORES_DATA desde el archivo de datos sin depender del PYTHONPATH."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, 'jugadores_mundial_2026_data_v2.py')

    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraer la lista JUGADORES_DATA
    start = content.find('JUGADORES_DATA = [')
    end = content.rfind(']')
    if start == -1 or end == -1:
        raise ValueError('No se encontró JUGADORES_DATA en el archivo de datos')

    namespace = {}
    exec(content[start:end + 1], namespace)
    return namespace['JUGADORES_DATA']


def seed_jugadores(apps, schema_editor):
    """Inserta los jugadores del Mundial 2026."""
    Jugador = apps.get_model('partidos', 'Jugador')
    Seleccion = apps.get_model('partidos', 'Seleccion')

    JUGADORES_DATA = _load_jugadores_data()

    # Cache de país -> id_seleccion para evitar N+1 queries
    seleccion_map = {
        sel.pais: sel.id_seleccion
        for sel in Seleccion.objects.all()
    }

    jugadores_objs = []
    for pais, dorsal, nombre, posicion in JUGADORES_DATA:
        fk_id_seleccion = seleccion_map.get(pais)
        if fk_id_seleccion is None:
            print(f"WARNING: No se encontró selección para país '{pais}'. Saltando jugador '{nombre}'.")
            continue

        jugadores_objs.append(Jugador(
            primer_nombre=nombre,
            dorsal=dorsal,
            posicion=posicion,
            fk_id_seleccion=fk_id_seleccion,
            status=True,
        ))

    Jugador.objects.bulk_create(jugadores_objs, batch_size=500)
    print(f"Insertados {len(jugadores_objs)} jugadores.")


def reverse_seed(apps, schema_editor):
    """Elimina los jugadores del Mundial 2026."""
    Jugador = apps.get_model('partidos', 'Jugador')
    Seleccion = apps.get_model('partidos', 'Seleccion')

    JUGADORES_DATA = _load_jugadores_data()
    paises = set(j[0] for j in JUGADORES_DATA)

    seleccion_ids = list(
        Seleccion.objects.filter(pais__in=paises)
        .values_list('id_seleccion', flat=True)
    )

    Jugador.objects.filter(fk_id_seleccion__in=seleccion_ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0015_seed_partidos_v2'),
    ]

    operations = [
        migrations.RunPython(seed_jugadores, reverse_seed),
    ]
