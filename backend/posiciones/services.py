"""
Servicio para calcular puntos de los usuarios según sus pronósticos.

Reglas de puntuación:
- 3 puntos: Acierta el resultado exacto (marcador exacto)
- 1 punto: No acierta el resultado exacto pero sí acierta el ganador (o empate)
- 0 puntos: No acierta nada
"""

from backend.pronosticos.models import Pronostico
from backend.partidos.models import Partido
from backend.posiciones.models import Ranking


def calcular_ganador(gol_local, gol_visitante, ganador_penales=None):
    """
    Determina el resultado de un partido.
    Retorna: 'local', 'visitante', o 'empate'
    """
    if gol_local is None or gol_visitante is None:
        return None
    
    if gol_local > gol_visitante:
        return 'local'
    elif gol_visitante > gol_local:
        return 'visitante'
    else:
        # Empate - si hay penales, determina el ganador
        if ganador_penales is not None:
            if ganador_penales == 1:  # Local ganó en penales
                return 'local_penales'
            else:
                return 'visitante_penales'
        return 'empate'


def calcular_puntos_pronostico(pronostico, partido):
    """
    Calcula los puntos obtenidos por un pronóstico comparado con el resultado real.
    
    Args:
        pronostico: Instancia de Pronostico
        partido: Instancia de Partido
    
    Returns:
        int: Puntos obtenidos (0, 1 o 3)
    """
    # Si el partido no tiene resultado aún, no hay puntos
    if partido.gol_local is None or partido.gol_visitante is None:
        return 0
    
    # Verificar resultado exacto (3 puntos)
    if (pronostico.gol_local == partido.gol_local and 
        pronostico.gol_visitante == partido.gol_visitante):
        return 3
    
    # Calcular ganadores para verificar si acertó el resultado (1 punto)
    ganador_pronostico = calcular_ganador(pronostico.gol_local, pronostico.gol_visitante)
    ganador_real = calcular_ganador(
        partido.gol_local, 
        partido.gol_visitante, 
        partido.ganador_penales
    )
    
    # Normalizar ganadores con penales
    if ganador_real in ('local_penales', 'visitante_penales'):
        ganador_real = ganador_real.replace('_penales', '')
    
    # Si acertó el ganador (o empate), 1 punto
    if ganador_pronostico == ganador_real:
        return 1
    
    # No acertó nada
    return 0


def calcular_posicion_usuario(usuario_id, liga_id):
    """
    Calcula la posición de un usuario en una liga sumando todos sus puntos.
    
    Args:
        usuario_id: ID del usuario
        liga_id: ID de la liga
    
    Returns:
        dict: Información de la posición del usuario
    """
    # Obtener todos los pronósticos del usuario en la liga
    pronosticos = Pronostico.objects.filter(
        fk_id_usuario=usuario_id,
        fk_id_liga=liga_id
    )
    
    total_puntos = 0
    partidos_pronosticados = 0
    aciertos_exactos = 0
    aciertos_ganador = 0
    
    for pronostico in pronosticos:
        try:
            partido = Partido.objects.get(id_partido=pronostico.fk_id_partido)
            
            # Solo contar partidos que ya tienen resultado
            if partido.gol_local is not None and partido.gol_visitante is not None:
                puntos = calcular_puntos_pronostico(pronostico, partido)
                total_puntos += puntos
                partidos_pronosticados += 1
                
                if puntos == 3:
                    aciertos_exactos += 1
                elif puntos == 1:
                    aciertos_ganador += 1
                    
        except Partido.DoesNotExist:
            continue
    
    return {
        'usuario_id': usuario_id,
        'liga_id': liga_id,
        'puntos': total_puntos,
        'pj': partidos_pronosticados,
        'aciertos_exactos': aciertos_exactos,
        'aciertos_ganador': aciertos_ganador
    }


def actualizar_ranking_usuario(usuario_id, liga_id):
    """
    Actualiza o crea el registro de ranking para un usuario en una liga.
    
    Args:
        usuario_id: ID del usuario
        liga_id: ID de la liga
    
    Returns:
        Ranking: Instancia del ranking actualizado
    """
    datos = calcular_posicion_usuario(usuario_id, liga_id)
    
    # Buscar o crear el registro de ranking
    ranking, creado = Ranking.objects.get_or_create(
        fk_id_usuario=usuario_id,
        fk_id_liga=liga_id,
        defaults={
            'puntos': datos['puntos'],
            'pj': datos['pj']
        }
    )
    
    # Si ya existe, actualizar
    if not creado:
        ranking.puntos = datos['puntos']
        ranking.pj = datos['pj']
        ranking.save()
    
    return ranking


def calcular_todas_las_posiciones(liga_id):
    """
    Calcula y actualiza las posiciones de todos los usuarios en una liga.
    
    Args:
        liga_id: ID de la liga
    
    Returns:
        list: Lista de rankings ordenados por puntos
    """
    from backend.ligas.models import Liga
    from backend.posiciones.models import Ranking
    
    # Obtener todos los usuarios que han hecho pronósticos en esta liga
    usuarios_ids = Pronostico.objects.filter(
        fk_id_liga=liga_id
    ).values_list('fk_id_usuario', flat=True).distinct()
    
    rankings = []
    for usuario_id in usuarios_ids:
        ranking = actualizar_ranking_usuario(usuario_id, liga_id)
        rankings.append(ranking)
    
    # Ordenar por puntos descendente
    rankings.sort(key=lambda x: x.puntos, reverse=True)
    
    return rankings


def obtener_ranking_con_posicion(liga_id):
    """
    Obtiene el ranking de una liga con la posición numérica de cada usuario,
    incluyendo la posición anterior y la variación (tendencia ↑↓→).

    Args:
        liga_id: ID de la liga

    Returns:
        list: Lista de diccionarios con ranking, posición y variación
    """
    rankings = calcular_todas_las_posiciones(liga_id)

    resultado = []
    posicion = 1
    puntos_anterior = None
    posicion_real = 1

    for ranking in rankings:
        # Si hay empate en puntos, mantener la misma posición
        if puntos_anterior is not None and ranking.puntos < puntos_anterior:
            posicion = posicion_real

        # Calcular variación y tendencia
        variacion = 0
        tendencia = 'igual'
        if ranking.posicion_anterior is not None and posicion is not None:
            variacion = ranking.posicion_anterior - posicion
            if variacion > 0:
                tendencia = 'subio'
            elif variacion < 0:
                tendencia = 'bajo'

        resultado.append({
            'posicion': posicion,
            'posicion_anterior': ranking.posicion_anterior,
            'variacion': variacion,
            'tendencia': tendencia,
            'usuario_id': ranking.fk_id_usuario,
            'puntos': ranking.puntos,
            'pj': ranking.pj,
            'fecha_actualizacion': ranking.fecha_actualizacion
        })

        puntos_anterior = ranking.puntos
        posicion_real += 1

    return resultado


# ---------------------------------------------------------------------------
# Tabla de posiciones de equipos (FIFA-style) por liga
# ---------------------------------------------------------------------------

def recalcular_tabla_equipos(liga_id):
    """
    Recalcula la tabla de posiciones de equipos para una liga específica.
    Usa todos los partidos finalizados de esa liga.
    Criterio FIFA: PTS > DG > GF
    """
    from backend.core.models import PosicionesTorneo
    from backend.partidos.models import Partido

    partidos = Partido.objects.filter(fk_id_liga=liga_id, estado_partido='finalizado')

    # Acumuladores por selección: {id_seleccion: {pg, pe, pp, gf, gc, pts}}
    stats = {}

    for p in partidos:
        local = p.equipo_local
        visitante = p.equipo_visitante

        for sid in (local, visitante):
            if sid not in stats:
                stats[sid] = {'pg': 0, 'pe': 0, 'pp': 0, 'gf': 0, 'gc': 0, 'pts': 0}

        gl, gv = p.gol_local or 0, p.gol_visitante or 0

        # goles
        stats[local]['gf'] += gl
        stats[local]['gc'] += gv
        stats[visitante]['gf'] += gv
        stats[visitante]['gc'] += gl

        # puntos
        if gl > gv:
            stats[local]['pg'] += 1
            stats[local]['pts'] += 3
            stats[visitante]['pp'] += 1
        elif gl < gv:
            stats[visitante]['pg'] += 1
            stats[visitante]['pts'] += 3
            stats[local]['pp'] += 1
        else:
            stats[local]['pe'] += 1
            stats[local]['pts'] += 1
            stats[visitante]['pe'] += 1
            stats[visitante]['pts'] += 1

    # Guardar posiciones anteriores antes de actualizar
    prev = {
        r.fk_id_seleccion: r.posicion
        for r in PosicionesTorneo.objects.filter(fk_id_liga=liga_id)
    }

    # Ordenar: puntos desc, dg desc, gf desc
    equipos = sorted(
        stats.items(),
        key=lambda x: (-x[1]['pts'], -(x[1]['gf'] - x[1]['gc']), -x[1]['gf'])
    )

    tabla = []
    for idx, (sid, s) in enumerate(equipos, start=1):
        obj, _ = PosicionesTorneo.objects.update_or_create(
            fk_id_liga=liga_id,
            fk_id_seleccion=sid,
            defaults={
                'pj': s['pg'] + s['pe'] + s['pp'],
                'pg': s['pg'],
                'pe': s['pe'],
                'pp': s['pp'],
                'gf': s['gf'],
                'gc': s['gc'],
                'dg': s['gf'] - s['gc'],
                'puntos': s['pts'],
                'posicion': idx,
                'posicion_anterior': prev.get(sid),
            }
        )
        tabla.append(obj)

    # Eliminar registros de equipos que ya no están en la liga (si aplica)
    selecciones_ids = set(stats.keys())
    PosicionesTorneo.objects.filter(fk_id_liga=liga_id).exclude(
        fk_id_seleccion__in=selecciones_ids
    ).delete()

    return tabla


def obtener_tabla_equipos(liga_id):
    """
    Devuelve la tabla de posiciones ordenada para una liga.
    """
    from backend.core.models import PosicionesTorneo
    return PosicionesTorneo.objects.filter(fk_id_liga=liga_id).order_by('posicion')


# ---------------------------------------------------------------------------
# Historial de rankings (snapshots por jornada)
# ---------------------------------------------------------------------------

def guardar_historial_ranking(liga_id):
    """
    Toma un snapshot del ranking actual de apostadores y lo guarda
    en HistorialRanking con la jornada = cantidad de partidos finalizados + 1.
    """
    from backend.posiciones.models import HistorialRanking
    from backend.partidos.models import Partido

    partidos_finalizados = Partido.objects.filter(
        fk_id_liga=liga_id, estado_partido='finalizado'
    ).count()
    jornada = partidos_finalizados or 1

    rankings = calcular_todas_las_posiciones(liga_id)

    for pos, ranking in enumerate(rankings, start=1):
        HistorialRanking.objects.create(
            fk_id_usuario=ranking.fk_id_usuario,
            fk_id_liga=liga_id,
            puntos=ranking.puntos,
            pj=ranking.pj,
            posicion=pos,
            jornada=jornada,
        )

    return jornada
