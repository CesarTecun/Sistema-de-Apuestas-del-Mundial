"""
Servicios para construir y manipular el bracket de eliminatorias.
"""

from backend.partidos.models import Partido, Seleccion
from backend.core.models import FaseGrupo


# Orden de fases eliminatorias para el bracket
FASES_ELIMINATORIAS = [
    'Octavos de Final',
    'Cuartos de Final',
    'Semifinales',
    'Tercer Lugar',
    'Final',
]

FASE_ORDER = {name: idx for idx, name in enumerate(FASES_ELIMINATORIAS)}


def _get_seleccion_info(seleccion_id):
    """Obtiene nombre y bandera de una selección por ID."""
    if not seleccion_id:
        return None
    try:
        s = Seleccion.objects.get(id_seleccion=seleccion_id)
        return {'id': s.id_seleccion, 'nombre': s.pais, 'bandera': s.bandera}
    except Seleccion.DoesNotExist:
        return {'id': seleccion_id, 'nombre': f'Equipo {seleccion_id}', 'bandera': None}


def _resolver_equipo(partido, campo_origen, campo_equipo):
    """
    Resuelve el equipo real de un partido.
    Si tiene partido origen, devuelve el ganador de ese partido.
    Si no, devuelve el equipo fijo.
    """
    origen_id = getattr(partido, campo_origen, None)
    equipo_fijo = getattr(partido, campo_equipo, None)

    if origen_id:
        try:
            origen = Partido.objects.get(id_partido=origen_id)
            ganador = origen.ganador
            if ganador:
                return {
                    'origen': {
                        'partido_id': origen.id_partido,
                        'slot': origen.slot_bracket,
                        'fase': _get_fase_nombre(origen.fk_id_fase),
                    },
                    'equipo': _get_seleccion_info(ganador),
                    'resuelto_por': 'ganador_partido_anterior'
                }
            else:
                return {
                    'origen': {
                        'partido_id': origen.id_partido,
                        'slot': origen.slot_bracket,
                        'fase': _get_fase_nombre(origen.fk_id_fase),
                    },
                    'equipo': None,
                    'resuelto_por': 'partido_pendiente'
                }
        except Partido.DoesNotExist:
            pass

    if equipo_fijo:
        return {
            'origen': None,
            'equipo': _get_seleccion_info(equipo_fijo),
            'resuelto_por': 'equipo_fijo'
        }

    return {
        'origen': None,
        'equipo': None,
        'resuelto_por': 'sin_definir'
    }


def _get_fase_nombre(fk_id_fase):
    """Obtiene el nombre de una fase por su ID."""
    if not fk_id_fase:
        return None
    try:
        return FaseGrupo.objects.get(id_fase=fk_id_fase).nombre_fase
    except FaseGrupo.DoesNotExist:
        return None


def _serializar_partido_bracket(partido):
    """Serializa un partido para mostrar en el bracket."""
    local = _resolver_equipo(partido, 'fk_partido_origen_local', 'equipo_local')
    visitante = _resolver_equipo(partido, 'fk_partido_origen_visitante', 'equipo_visitante')

    ganador_id = None
    if partido.estado_partido == 'finalizado':
        ganador_id = partido.ganador

    return {
        'id_partido': partido.id_partido,
        'slot': partido.slot_bracket,
        'horario': partido.horario.isoformat() if partido.horario else None,
        'fk_id_fase': partido.fk_id_fase,
        'fase': _get_fase_nombre(partido.fk_id_fase),
        'fk_id_sede': partido.fk_sede,
        'equipo_local': local,
        'equipo_visitante': visitante,
        'gol_local': partido.gol_local,
        'gol_visitante': partido.gol_visitante,
        'ganador_penales': partido.ganador_penales,
        'resultado': partido.resultado,
        'resultado_display': partido.resultado_display,
        'estado_partido': partido.estado_partido,
        'ganador': _get_seleccion_info(ganador_id) if ganador_id else None,
        'tipo_partido': partido.tipo_partido,
    }


def obtener_bracket(liga_id):
    """
    Construye el bracket de eliminatorias completo para una liga.

    Retorna:
        dict con estructura jerárquica del bracket agrupada por fase.
    """
    # Obtener IDs de fases eliminatorias
    fases_ids = list(
        FaseGrupo.objects
        .filter(nombre_fase__in=FASES_ELIMINATORIAS)
        .values_list('id_fase', flat=True)
    )

    if not fases_ids:
        return {
            'liga_id': liga_id,
            'error': 'No hay fases eliminatorias configuradas'
        }

    # Obtener partidos eliminatorios de la liga
    partidos = Partido.objects.filter(
        fk_id_liga=liga_id,
        fk_id_fase__in=fases_ids,
        status=True
    ).order_by('slot_bracket', 'horario')

    # Agrupar por fase
    fases_dict = {}
    for p in partidos:
        nombre_fase = _get_fase_nombre(p.fk_id_fase)
        if not nombre_fase:
            continue
        if nombre_fase not in fases_dict:
            fases_dict[nombre_fase] = []
        fases_dict[nombre_fase].append(_serializar_partido_bracket(p))

    # Ordenar fases según FASE_ORDER
    fases_ordenadas = []
    for nombre in FASES_ELIMINATORIAS:
        if nombre in fases_dict:
            fases_ordenadas.append({
                'nombre': nombre,
                'orden': FASE_ORDER[nombre],
                'partidos': fases_dict[nombre]
            })

    return {
        'liga_id': liga_id,
        'total_partidos': partidos.count(),
        'fases': fases_ordenadas
    }


def generar_cruces_eliminatoria(liga_id, partidos_octavos_config):
    """
    Genera automáticamente los cruces de eliminatoria (octavos -> cuartos -> semis -> final).

    Args:
        liga_id: ID de la liga
        partidos_octavos_config: lista de dicts con:
            {
                'slot': 'O1',
                'equipo_local': seleccion_id,
                'equipo_visitante': seleccion_id,
                'horario': datetime,
                'fk_sede': sede_id
            }
    Retorna:
        dict con los IDs de los partidos creados.
    """
    from django.utils import timezone

    # Obtener fases
    fases = {
        f.nombre_fase: f.id_fase
        for f in FaseGrupo.objects.filter(nombre_fase__in=FASES_ELIMINATORIAS)
    }

    if not all(k in fases for k in FASES_ELIMINATORIAS):
        return {'error': 'Faltan fases eliminatorias configuradas'}

    creados = {}

    # --- Octavos ---
    octavos = []
    for cfg in partidos_octavos_config:
        p = Partido.objects.create(
            horario=cfg.get('horario', timezone.now()),
            equipo_local=cfg.get('equipo_local') or 0,
            equipo_visitante=cfg.get('equipo_visitante') or 0,
            fk_sede=cfg.get('fk_sede'),
            fk_id_fase=fases['Octavos de Final'],
            fk_id_liga=liga_id,
            slot_bracket=cfg['slot'],
            tipo_partido='Eliminatoria'
        )
        octavos.append(p)
        creados[cfg['slot']] = p.id_partido

    # Mapeo de slots de octavos a cuartos
    # O1 ganador vs O2 ganador -> C1
    # O3 ganador vs O4 ganador -> C2
    # O5 ganador vs O6 ganador -> C3
    # O7 ganador vs O8 ganador -> C4
    cruces_cuartos = [
        ('C1', ['O1', 'O2']),
        ('C2', ['O3', 'O4']),
        ('C3', ['O5', 'O6']),
        ('C4', ['O7', 'O8']),
    ]

    for slot, origenes in cruces_cuartos:
        ids_origen = [creados.get(o) for o in origenes if creados.get(o)]
        p = Partido.objects.create(
            horario=timezone.now(),
            equipo_local=0,
            equipo_visitante=0,
            fk_id_fase=fases['Cuartos de Final'],
            fk_id_liga=liga_id,
            slot_bracket=slot,
            tipo_partido='Eliminatoria',
            fk_partido_origen_local=ids_origen[0] if len(ids_origen) > 0 else None,
            fk_partido_origen_visitante=ids_origen[1] if len(ids_origen) > 1 else None,
        )
        creados[slot] = p.id_partido

    # Semifinales
    # C1 ganador vs C2 ganador -> S1
    # C3 ganador vs C4 ganador -> S2
    cruces_semis = [
        ('S1', ['C1', 'C2']),
        ('S2', ['C3', 'C4']),
    ]

    for slot, origenes in cruces_semis:
        ids_origen = [creados.get(o) for o in origenes if creados.get(o)]
        p = Partido.objects.create(
            horario=timezone.now(),
            equipo_local=0,
            equipo_visitante=0,
            fk_id_fase=fases['Semifinales'],
            fk_id_liga=liga_id,
            slot_bracket=slot,
            tipo_partido='Eliminatoria',
            fk_partido_origen_local=ids_origen[0] if len(ids_origen) > 0 else None,
            fk_partido_origen_visitante=ids_origen[1] if len(ids_origen) > 1 else None,
        )
        creados[slot] = p.id_partido

    # Final: S1 ganador vs S2 ganador -> F1
    ids_semis = [creados.get(s) for s in ['S1', 'S2'] if creados.get(s)]
    p_final = Partido.objects.create(
        horario=timezone.now(),
        equipo_local=0,
        equipo_visitante=0,
        fk_id_fase=fases['Final'],
        fk_id_liga=liga_id,
        slot_bracket='F1',
        tipo_partido='Eliminatoria',
        fk_partido_origen_local=ids_semis[0] if len(ids_semis) > 0 else None,
        fk_partido_origen_visitante=ids_semis[1] if len(ids_semis) > 1 else None,
    )
    creados['F1'] = p_final.id_partido

    # Tercer Lugar: S1 perdedor vs S2 perdedor -> T1
    p_tercer = Partido.objects.create(
        horario=timezone.now(),
        equipo_local=0,
        equipo_visitante=0,
        fk_id_fase=fases['Tercer Lugar'],
        fk_id_liga=liga_id,
        slot_bracket='T1',
        tipo_partido='Eliminatoria',
        fk_partido_origen_local=ids_semis[0] if len(ids_semis) > 0 else None,
        fk_partido_origen_visitante=ids_semis[1] if len(ids_semis) > 1 else None,
    )
    creados['T1'] = p_tercer.id_partido

    return {
        'liga_id': liga_id,
        'partidos_creados': creados,
        'total': len(creados)
    }
