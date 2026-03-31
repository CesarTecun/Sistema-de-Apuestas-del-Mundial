"""
Servicios para calcular y distribuir premios en las ligas.

Distribución estándar:
- 1er Lugar: 50%
- 2do Lugar: 25%
- 3er Lugar: 10%
- Último Lugar: 10%
"""

from decimal import Decimal
from backend.premios.models import Premio
from backend.ligas.models import Liga
from backend.posiciones.models import Ranking
from backend.posiciones.services import obtener_ranking_con_posicion


# Distribución por defecto de premios
DISTRIBUCION_DEFAULT = {
    1: Decimal('50.00'),   # Primer lugar: 50%
    2: Decimal('25.00'),   # Segundo lugar: 25%
    3: Decimal('10.00'),   # Tercer lugar: 10%
    -1: Decimal('10.00'),  # Último lugar: 10% (-1 representa último)
}


def inicializar_premios_liga(liga_id, distribucion=None):
    """
    Inicializa la configuración de premios para una liga.
    Crea los registros de premios según la distribución especificada.
    
    Args:
        liga_id: ID de la liga
        distribucion: Dict con {posicion: porcentaje}. Si es None, usa DISTRIBUCION_DEFAULT
    
    Returns:
        list: Lista de objetos Premio creados
    """
    if distribucion is None:
        distribucion = DISTRIBUCION_DEFAULT
    
    premios_creados = []
    
    for posicion, porcentaje in distribucion.items():
        premio, creado = Premio.objects.get_or_create(
            fk_id_liga=liga_id,
            posicion=posicion,
            defaults={'porcentaje_premio': porcentaje}
        )
        if creado:
            premios_creados.append(premio)
    
    return premios_creados


def calcular_monto_premio(monto_total, porcentaje):
    """
    Calcula el monto del premio basado en el total y el porcentaje.
    
    Args:
        monto_total: Monto total recaudado (Decimal o float)
        porcentaje: Porcentaje del premio (Decimal o float)
    
    Returns:
        Decimal: Monto calculado
    """
    monto_total = Decimal(str(monto_total))
    porcentaje = Decimal(str(porcentaje))
    return (monto_total * porcentaje) / Decimal('100')


def obtener_distribucion_premios_liga(liga_id):
    """
    Obtiene la distribución de premios configurada para una liga.
    
    Args:
        liga_id: ID de la liga
    
    Returns:
        dict: {posicion: porcentaje}
    """
    premios = Premio.objects.filter(fk_id_liga=liga_id)
    
    if not premios.exists():
        # Si no hay premios configurados, inicializar con distribución default
        inicializar_premios_liga(liga_id)
        premios = Premio.objects.filter(fk_id_liga=liga_id)
    
    return {p.posicion: p.porcentaje_premio for p in premios}


def calcular_premios_liga(liga_id):
    """
    Calcula los premios para todos los ganadores de una liga.
    Obtiene las posiciones del ranking y calcula los montos correspondientes.
    
    Args:
        liga_id: ID de la liga
    
    Returns:
        dict: Información completa de premios y ganadores
    """
    try:
        liga = Liga.objects.get(id_liga=liga_id)
    except Liga.DoesNotExist:
        return {'error': f'La liga {liga_id} no existe'}
    
    monto_total = liga.monto_total_recaudado or Decimal('0')
    
    if monto_total <= 0:
        return {
            'liga_id': liga_id,
            'nombre_liga': liga.nombre_liga,
            'monto_total': monto_total,
            'error': 'No hay monto recaudado para distribuir premios'
        }
    
    # Obtener distribución de premios
    distribucion = obtener_distribucion_premios_liga(liga_id)
    
    # Obtener ranking de la liga
    ranking = obtener_ranking_con_posicion(liga_id)
    
    if not ranking:
        return {
            'liga_id': liga_id,
            'nombre_liga': liga.nombre_liga,
            'monto_total': monto_total,
            'error': 'No hay participantes en el ranking de esta liga'
        }
    
    # Calcular premios para cada posición
    premios_calculados = []
    total_participantes = len(ranking)
    
    for posicion_data in ranking:
        posicion = posicion_data['posicion']
        usuario_id = posicion_data['usuario_id']
        puntos = posicion_data['puntos']
        
        # Verificar si hay premio para esta posición
        porcentaje = None
        if posicion in distribucion:
            porcentaje = distribucion[posicion]
        elif posicion == total_participantes and -1 in distribucion:
            # Último lugar (representado como -1 en la configuración)
            porcentaje = distribucion[-1]
        
        if porcentaje:
            monto_premio = calcular_monto_premio(monto_total, porcentaje)
            premios_calculados.append({
                'posicion': posicion,
                'usuario_id': usuario_id,
                'puntos': puntos,
                'porcentaje': float(porcentaje),
                'monto_premio': float(monto_premio)
            })
    
    # Calcular totales distribuidos y remanente
    total_distribuido = sum(p['monto_premio'] for p in premios_calculados)
    remanente = float(monto_total) - total_distribuido
    
    return {
        'liga_id': liga_id,
        'nombre_liga': liga.nombre_liga,
        'monto_total_recaudado': float(monto_total),
        'total_participantes': total_participantes,
        'premios': premios_calculados,
        'total_distribuido': total_distribuido,
        'remanente': remanente
    }


def obtener_premio_usuario(liga_id, usuario_id):
    """
    Obtiene el premio correspondiente a un usuario específico en una liga.
    
    Args:
        liga_id: ID de la liga
        usuario_id: ID del usuario
    
    Returns:
        dict: Información del premio del usuario o None si no tiene premio
    """
    # Obtener el ranking completo con premios
    resultado = calcular_premios_liga(liga_id)
    
    if 'error' in resultado:
        return resultado
    
    # Buscar al usuario en los premios
    for premio in resultado.get('premios', []):
        if premio['usuario_id'] == usuario_id:
            return {
                'liga_id': liga_id,
                'usuario_id': usuario_id,
                'posicion': premio['posicion'],
                'puntos': premio['puntos'],
                'porcentaje': premio['porcentaje'],
                'monto_premio': premio['monto_premio'],
                'monto_total_liga': resultado['monto_total_recaudado']
            }
    
    return {
        'liga_id': liga_id,
        'usuario_id': usuario_id,
        'mensaje': 'No tienes premio en esta liga',
        'posicion': None,
        'monto_premio': 0
    }


def actualizar_distribucion_premios(liga_id, nueva_distribucion):
    """
    Actualiza la distribución de premios para una liga.
    
    Args:
        liga_id: ID de la liga
        nueva_distribucion: Dict {posicion: porcentaje}
    
    Returns:
        list: Lista de premios actualizados
    """
    premios_actualizados = []
    
    # Eliminar premios existentes
    Premio.objects.filter(fk_id_liga=liga_id).delete()
    
    # Crear nuevos premios
    for posicion, porcentaje in nueva_distribucion.items():
        premio = Premio.objects.create(
            fk_id_liga=liga_id,
            posicion=posicion,
            porcentaje_premio=Decimal(str(porcentaje))
        )
        premios_actualizados.append(premio)
    
    return premios_actualizados
