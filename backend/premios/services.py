"""
Servicios para calcular y distribuir premios en las ligas.

Reglas de distribucion:
- 1er Lugar: 50%
- 2do Lugar: 25%
- 3er Lugar: 10%
- Ultimo Lugar: 10%
- Plataforma: 5%

De ese 5% de plataforma:
- 1% del total de TODAS las ligas para premios globales:
  - 0.5% para los primeros 3 lugares individuales de todas las ligas
  - 0.5% para la liga con mayor promedio de puntos (repartido a sus participantes)

Reglas de empate:
- Empate en 1ro: 85% (50+25+10) repartido equitativo entre empatados. Ultimo sigue con 10%.
- Empate en 2do: 35% (25+10) repartido equitativo. 1ro=50%, ultimo=10%.
- Empate en 3ro: 10% repartido equitativo. 1ro=50%, 2do=25%, ultimo=10%.
- Empate en ultimo: 10% repartido equitativo.
"""

from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from backend.premios.models import Premio
from backend.ligas.models import Liga, ParticipanteLiga
from backend.posiciones.models import Ranking
from backend.posiciones.services import obtener_ranking_con_posicion
from backend.historialganador.models import HistorialGanador


# Distribucion por defecto de premios locales
DISTRIBUCION_DEFAULT = {
    1: Decimal('50.00'),
    2: Decimal('25.00'),
    3: Decimal('10.00'),
    -1: Decimal('10.00'),
}

# Porcentajes globales
PORCENTAJE_GLOBAL_TOTAL = Decimal('1.00')  # 1% del total de todas las ligas
PORCENTAJE_GLOBAL_INDIVIDUAL = Decimal('0.50')  # 0.5% para top 3 individuales
PORCENTAJE_GLOBAL_LIGA = Decimal('0.50')  # 0.5% para liga con mayor promedio

# Sub-distribucion del 0.5% individual (mismas reglas 50/25/10)
DISTRIBUCION_GLOBAL_INDIVIDUAL = {
    1: Decimal('50.00'),
    2: Decimal('25.00'),
    3: Decimal('10.00'),
}


def _agrupar_ranking_por_posicion(ranking):
    """Agrupa el ranking por posicion para detectar empates."""
    from collections import defaultdict
    grupos = defaultdict(list)
    for item in ranking:
        grupos[item['posicion']].append(item)
    return dict(grupos)


def _identificar_ultimo_lugar(ranking):
    """Identifica el/los usuario(s) en ultimo lugar."""
    if not ranking:
        return []
    puntos_min = min(r['puntos'] for r in ranking)
    return [r for r in ranking if r['puntos'] == puntos_min]


def calcular_premios_locales_con_empates(liga_id):
    """
    Calcula los premios locales de una liga considerando TODOS los casos de empate.

    Retorna lista de dicts: [{usuario_id, posicion, puntos, porcentaje, monto_premio, detalle}]
    """
    try:
        liga = Liga.objects.get(id_liga=liga_id)
    except Liga.DoesNotExist:
        return None, {'error': f'La liga {liga_id} no existe'}

    monto_total = liga.monto_total_recaudado or Decimal('0')
    if monto_total <= 0:
        return None, {'error': 'No hay monto recaudado para distribuir premios'}

    ranking = obtener_ranking_con_posicion(liga_id)
    if not ranking:
        return None, {'error': 'No hay participantes en el ranking de esta liga'}

    total_participantes = len(ranking)
    grupos = _agrupar_ranking_por_posicion(ranking)
    ultimos = _identificar_ultimo_lugar(ranking)
    cantidad_ultimos = len(ultimos)

    # Detectar empates en cada posicion premiada
    empate_1ro = len(grupos.get(1, [])) > 1
    empate_2do = len(grupos.get(2, [])) > 1 if 2 in grupos else False
    empate_3ro = len(grupos.get(3, [])) > 1 if 3 in grupos else False
    empate_ultimo = cantidad_ultimos > 1

    premios = []

    # --- Empate en 1ro ---
    if empate_1ro:
        ganadores_1ro = grupos[1]
        monto_85 = (monto_total * Decimal('85.00')) / Decimal('100')
        monto_por_ganador = monto_85 / Decimal(len(ganadores_1ro))
        for g in ganadores_1ro:
            premios.append({
                'usuario_id': g['usuario_id'],
                'posicion': 1,
                'puntos': g['puntos'],
                'porcentaje': Decimal('85.00') / Decimal(len(ganadores_1ro)),
                'monto_premio': monto_por_ganador.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': f'Empate 1ro - {len(ganadores_1ro)} ganadores'
            })
        # Ultimo lugar (si no esta empatado en 1ro y no es parte del empate)
        if cantidad_ultimos >= 1 and not any(u['usuario_id'] == ganadores_1ro[0]['usuario_id'] for u in ultimos):
            monto_ult = (monto_total * Decimal('10.00')) / Decimal('100')
            if empate_ultimo:
                monto_u = monto_ult / Decimal(cantidad_ultimos)
                for u in ultimos:
                    premios.append({
                        'usuario_id': u['usuario_id'],
                        'posicion': -1,
                        'puntos': u['puntos'],
                        'porcentaje': Decimal('10.00') / Decimal(cantidad_ultimos),
                        'monto_premio': monto_u.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                        'detalle': f'Empate ultimo - {cantidad_ultimos} ganadores'
                    })
            else:
                premios.append({
                    'usuario_id': ultimos[0]['usuario_id'],
                    'posicion': -1,
                    'puntos': ultimos[0]['puntos'],
                    'porcentaje': Decimal('10.00'),
                    'monto_premio': monto_ult.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                    'detalle': 'Ultimo lugar'
                })

    # --- Empate en 2do (sin empate en 1ro) ---
    elif empate_2do:
        ganadores_2do = grupos[2]
        monto_35 = (monto_total * Decimal('35.00')) / Decimal('100')
        monto_por_ganador = monto_35 / Decimal(len(ganadores_2do))
        for g in ganadores_2do:
            premios.append({
                'usuario_id': g['usuario_id'],
                'posicion': 2,
                'puntos': g['puntos'],
                'porcentaje': Decimal('35.00') / Decimal(len(ganadores_2do)),
                'monto_premio': monto_por_ganador.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': f'Empate 2do - {len(ganadores_2do)} ganadores'
            })
        # 1ro
        if 1 in grupos:
            g1 = grupos[1][0]
            monto_1ro = (monto_total * Decimal('50.00')) / Decimal('100')
            premios.append({
                'usuario_id': g1['usuario_id'],
                'posicion': 1,
                'puntos': g1['puntos'],
                'porcentaje': Decimal('50.00'),
                'monto_premio': monto_1ro.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': 'Primer lugar'
            })
        # Ultimo
        if cantidad_ultimos >= 1:
            monto_ult = (monto_total * Decimal('10.00')) / Decimal('100')
            if empate_ultimo:
                monto_u = monto_ult / Decimal(cantidad_ultimos)
                for u in ultimos:
                    premios.append({
                        'usuario_id': u['usuario_id'],
                        'posicion': -1,
                        'puntos': u['puntos'],
                        'porcentaje': Decimal('10.00') / Decimal(cantidad_ultimos),
                        'monto_premio': monto_u.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                        'detalle': f'Empate ultimo - {cantidad_ultimos} ganadores'
                    })
            else:
                premios.append({
                    'usuario_id': ultimos[0]['usuario_id'],
                    'posicion': -1,
                    'puntos': ultimos[0]['puntos'],
                    'porcentaje': Decimal('10.00'),
                    'monto_premio': monto_ult.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                    'detalle': 'Ultimo lugar'
                })

    # --- Empate en 3ro (sin empate en 1ro ni 2do) ---
    elif empate_3ro:
        ganadores_3ro = grupos[3]
        monto_10 = (monto_total * Decimal('10.00')) / Decimal('100')
        monto_por_ganador = monto_10 / Decimal(len(ganadores_3ro))
        for g in ganadores_3ro:
            premios.append({
                'usuario_id': g['usuario_id'],
                'posicion': 3,
                'puntos': g['puntos'],
                'porcentaje': Decimal('10.00') / Decimal(len(ganadores_3ro)),
                'monto_premio': monto_por_ganador.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': f'Empate 3ro - {len(ganadores_3ro)} ganadores'
            })
        # 1ro y 2do
        if 1 in grupos:
            g1 = grupos[1][0]
            monto_1ro = (monto_total * Decimal('50.00')) / Decimal('100')
            premios.append({
                'usuario_id': g1['usuario_id'],
                'posicion': 1,
                'puntos': g1['puntos'],
                'porcentaje': Decimal('50.00'),
                'monto_premio': monto_1ro.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': 'Primer lugar'
            })
        if 2 in grupos:
            g2 = grupos[2][0]
            monto_2do = (monto_total * Decimal('25.00')) / Decimal('100')
            premios.append({
                'usuario_id': g2['usuario_id'],
                'posicion': 2,
                'puntos': g2['puntos'],
                'porcentaje': Decimal('25.00'),
                'monto_premio': monto_2do.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': 'Segundo lugar'
            })
        # Ultimo
        if cantidad_ultimos >= 1:
            monto_ult = (monto_total * Decimal('10.00')) / Decimal('100')
            if empate_ultimo:
                monto_u = monto_ult / Decimal(cantidad_ultimos)
                for u in ultimos:
                    premios.append({
                        'usuario_id': u['usuario_id'],
                        'posicion': -1,
                        'puntos': u['puntos'],
                        'porcentaje': Decimal('10.00') / Decimal(cantidad_ultimos),
                        'monto_premio': monto_u.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                        'detalle': f'Empate ultimo - {cantidad_ultimos} ganadores'
                    })
            else:
                premios.append({
                    'usuario_id': ultimos[0]['usuario_id'],
                    'posicion': -1,
                    'puntos': ultimos[0]['puntos'],
                    'porcentaje': Decimal('10.00'),
                    'monto_premio': monto_ult.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                    'detalle': 'Ultimo lugar'
                })

    # --- Sin empates en posiciones premiadas (solo ultimo puede empatar) ---
    else:
        # 1ro
        if 1 in grupos:
            g1 = grupos[1][0]
            monto_1ro = (monto_total * Decimal('50.00')) / Decimal('100')
            premios.append({
                'usuario_id': g1['usuario_id'],
                'posicion': 1,
                'puntos': g1['puntos'],
                'porcentaje': Decimal('50.00'),
                'monto_premio': monto_1ro.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': 'Primer lugar'
            })
        # 2do
        if 2 in grupos:
            g2 = grupos[2][0]
            monto_2do = (monto_total * Decimal('25.00')) / Decimal('100')
            premios.append({
                'usuario_id': g2['usuario_id'],
                'posicion': 2,
                'puntos': g2['puntos'],
                'porcentaje': Decimal('25.00'),
                'monto_premio': monto_2do.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': 'Segundo lugar'
            })
        # 3ro
        if 3 in grupos:
            g3 = grupos[3][0]
            monto_3ro = (monto_total * Decimal('10.00')) / Decimal('100')
            premios.append({
                'usuario_id': g3['usuario_id'],
                'posicion': 3,
                'puntos': g3['puntos'],
                'porcentaje': Decimal('10.00'),
                'monto_premio': monto_3ro.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': 'Tercer lugar'
            })
        # Ultimo
        if cantidad_ultimos >= 1:
            monto_ult = (monto_total * Decimal('10.00')) / Decimal('100')
            if empate_ultimo:
                monto_u = monto_ult / Decimal(cantidad_ultimos)
                for u in ultimos:
                    premios.append({
                        'usuario_id': u['usuario_id'],
                        'posicion': -1,
                        'puntos': u['puntos'],
                        'porcentaje': Decimal('10.00') / Decimal(cantidad_ultimos),
                        'monto_premio': monto_u.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                        'detalle': f'Empate ultimo - {cantidad_ultimos} ganadores'
                    })
            else:
                premios.append({
                    'usuario_id': ultimos[0]['usuario_id'],
                    'posicion': -1,
                    'puntos': ultimos[0]['puntos'],
                    'porcentaje': Decimal('10.00'),
                    'monto_premio': monto_ult.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                    'detalle': 'Ultimo lugar'
                })

    # Totales
    total_distribuido = sum(p['monto_premio'] for p in premios)
    plataforma = (monto_total * Decimal('5.00')) / Decimal('100')

    return premios, {
        'liga_id': liga_id,
        'nombre_liga': liga.nombre_liga,
        'monto_total_recaudado': float(monto_total.quantize(Decimal('0.01'))),
        'total_participantes': total_participantes,
        'premios': [{k: float(v) if isinstance(v, Decimal) else v for k, v in p.items()} for p in premios],
        'total_distribuido': float(total_distribuido.quantize(Decimal('0.01'))),
        'monto_plataforma': float(plataforma.quantize(Decimal('0.01'))),
        'empates': {
            'primer_lugar': empate_1ro,
            'segundo_lugar': empate_2do,
            'tercer_lugar': empate_3ro,
            'ultimo_lugar': empate_ultimo,
        }
    }


def calcular_premios_globales():
    """
    Calcula los premios globales sobre el 1% del monto total recaudado de TODAS las ligas de apuesta.

    Retorna: (lista de premios individuales, lista de premios por liga, resumen)
    """
    # Obtener todas las ligas con monto recaudado > 0 (ligas de apuesta)
    ligas = Liga.objects.filter(monto_total_recaudado__gt=0, estado='Activa')
    if not ligas.exists():
        return [], [], {'error': 'No hay ligas de apuesta activas'}

    monto_total_global = sum(l.monto_total_recaudado for l in ligas)
    monto_global = (monto_total_global * PORCENTAJE_GLOBAL_TOTAL) / Decimal('100')
    monto_individual = (monto_global * PORCENTAJE_GLOBAL_INDIVIDUAL) / Decimal('100')
    monto_por_liga = (monto_global * PORCENTAJE_GLOBAL_LIGA) / Decimal('100')

    # --- 0.5% para top 3 individuales globales ---
    # Obtener todos los rankings de todas las ligas de apuesta
    todos_rankings = []
    for liga in ligas:
        ranking = obtener_ranking_con_posicion(liga.id_liga)
        for r in ranking:
            todos_rankings.append({
                'usuario_id': r['usuario_id'],
                'liga_id': liga.id_liga,
                'puntos': r['puntos'],
                'liga_nombre': liga.nombre_liga,
            })

    # Ordenar por puntos descendentemente
    todos_rankings.sort(key=lambda x: x['puntos'], reverse=True)

    # Agrupar por puntos para detectar empates globales
    from collections import defaultdict
    grupos_global = defaultdict(list)
    for r in todos_rankings:
        grupos_global[r['puntos']].append(r)

    # Asignar posiciones globales
    posicion_global = 1
    pos_real = 1
    puntos_anterior = None
    rankings_global = []
    for r in todos_rankings:
        if puntos_anterior is not None and r['puntos'] < puntos_anterior:
            posicion_global = pos_real
        rankings_global.append({**r, 'posicion': posicion_global})
        puntos_anterior = r['puntos']
        pos_real += 1

    grupos_pos = defaultdict(list)
    for r in rankings_global:
        grupos_pos[r['posicion']].append(r)

    premios_individuales = []
    # 1ro global
    if 1 in grupos_pos:
        ganadores = grupos_pos[1]
        monto = (monto_individual * Decimal('50.00')) / Decimal('100')
        m_por_ganador = monto / Decimal(len(ganadores))
        for g in ganadores:
            premios_individuales.append({
                'usuario_id': g['usuario_id'],
                'liga_id': g['liga_id'],
                'posicion': 1,
                'puntos': g['puntos'],
                'porcentaje_del_global': Decimal('50.00') / Decimal(len(ganadores)),
                'monto_premio': m_por_ganador.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': f'1er lugar global - {len(ganadores)} ganadores' if len(ganadores) > 1 else '1er lugar global',
            })
    # 2do global
    if 2 in grupos_pos:
        ganadores = grupos_pos[2]
        monto = (monto_individual * Decimal('25.00')) / Decimal('100')
        m_por_ganador = monto / Decimal(len(ganadores))
        for g in ganadores:
            premios_individuales.append({
                'usuario_id': g['usuario_id'],
                'liga_id': g['liga_id'],
                'posicion': 2,
                'puntos': g['puntos'],
                'porcentaje_del_global': Decimal('25.00') / Decimal(len(ganadores)),
                'monto_premio': m_por_ganador.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': f'2do lugar global - {len(ganadores)} ganadores' if len(ganadores) > 1 else '2do lugar global',
            })
    # 3ro global
    if 3 in grupos_pos:
        ganadores = grupos_pos[3]
        monto = (monto_individual * Decimal('10.00')) / Decimal('100')
        m_por_ganador = monto / Decimal(len(ganadores))
        for g in ganadores:
            premios_individuales.append({
                'usuario_id': g['usuario_id'],
                'liga_id': g['liga_id'],
                'posicion': 3,
                'puntos': g['puntos'],
                'porcentaje_del_global': Decimal('10.00') / Decimal(len(ganadores)),
                'monto_premio': m_por_ganador.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'detalle': f'3er lugar global - {len(ganadores)} ganadores' if len(ganadores) > 1 else '3er lugar global',
            })

    # --- 0.5% para la liga con mayor promedio de puntos ---
    ligas_promedio = []
    for liga in ligas:
        rankings = obtener_ranking_con_posicion(liga.id_liga)
        if rankings:
            total_puntos = sum(r['puntos'] for r in rankings)
            promedio = Decimal(str(total_puntos)) / Decimal(len(rankings))
            ligas_promedio.append({
                'liga_id': liga.id_liga,
                'nombre_liga': liga.nombre_liga,
                'promedio': float(promedio),
                'total_puntos': total_puntos,
                'participantes': len(rankings),
            })

    premios_liga = []
    if ligas_promedio:
        ligas_promedio.sort(key=lambda x: x['promedio'], reverse=True)
        liga_ganadora = ligas_promedio[0]
        # Verificar empate en promedio
        empates_promedio = [l for l in ligas_promedio if l['promedio'] == liga_ganadora['promedio']]
        monto_por_liga_empate = monto_por_liga / Decimal(len(empates_promedio))
        for liga_emp in empates_promedio:
            # Distribuir equitativamente entre todos los participantes de la liga
            participantes = Ranking.objects.filter(fk_id_liga=liga_emp['liga_id'], status=True)
            cantidad = participantes.count()
            if cantidad > 0:
                monto_por_participante = monto_por_liga_empate / Decimal(cantidad)
                for p in participantes:
                    premios_liga.append({
                        'usuario_id': p.fk_id_usuario,
                        'liga_id': liga_emp['liga_id'],
                        'posicion': None,
                        'puntos': p.puntos,
                        'porcentaje_del_global': (PORCENTAJE_GLOBAL_LIGA / Decimal(len(empates_promedio))) / Decimal(cantidad),
                        'monto_premio': monto_por_participante.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                        'detalle': f'Liga con mayor promedio ({liga_emp["promedio"]:.2f} pts) - {len(empates_promedio)} ligas empatadas' if len(empates_promedio) > 1 else f'Liga con mayor promedio ({liga_emp["promedio"]:.2f} pts)',
                    })

    total_individual = sum(p['monto_premio'] for p in premios_individuales)
    total_liga = sum(p['monto_premio'] for p in premios_liga)

    resumen = {
        'monto_total_global': float(monto_total_global.quantize(Decimal('0.01'))),
        'monto_premios_globales': float(monto_global.quantize(Decimal('0.01'))),
        'monto_individual_global': float(monto_individual.quantize(Decimal('0.01'))),
        'monto_liga_global': float(monto_por_liga.quantize(Decimal('0.01'))),
        'total_premios_individuales': float(total_individual.quantize(Decimal('0.01'))),
        'total_premios_por_liga': float(total_liga.quantize(Decimal('0.01'))),
        'total_distribuido_global': float((total_individual + total_liga).quantize(Decimal('0.01'))),
        'liga_mayor_promedio': ligas_promedio[0] if ligas_promedio else None,
    }

    return premios_individuales, premios_liga, resumen


def cerrar_liga(liga_id):
    """
    Ejecuta el cierre completo de una liga:
    1. Calcula premios locales con empates
    2. Calcula premios globales (sobre el 1% total)
    3. Registra todo en HistorialGanador
    4. Marca la liga como cerrada

    Retorna dict con resumen completo.
    """
    with transaction.atomic():
        try:
            liga = Liga.objects.get(id_liga=liga_id)
        except Liga.DoesNotExist:
            return {'error': f'La liga {liga_id} no existe'}

        if liga.estado == 'Cerrada':
            return {'error': 'La liga ya fue cerrada anteriormente'}

        # Calcular premios locales
        premios_locales, resumen_local = calcular_premios_locales_con_empates(liga_id)
        if premios_locales is None:
            return resumen_local

        # Calcular premios globales
        premios_individuales, premios_liga, resumen_global = calcular_premios_globales()

        total_premio_liga = Decimal('0')

        # Registrar premios locales en HistorialGanador y sumar al total
        for p in premios_locales:
            HistorialGanador.objects.create(
                fk_id_usuario=p['usuario_id'],
                fk_id_liga=liga_id,
                monto_pagado=p['monto_premio'],
                tipo_premio='Local',
                posicion=p['posicion'],
                porcentaje=p['porcentaje'],
                detalle=p['detalle'],
            )
            total_premio_liga += p['monto_premio']

        # Registrar retencion de plataforma (NO se suma al premio total entregado)
        monto_plataforma = Decimal(str(resumen_local['monto_plataforma']))
        HistorialGanador.objects.create(
            fk_id_usuario=None,
            fk_id_liga=liga_id,
            monto_pagado=monto_plataforma,
            tipo_premio='Plataforma',
            posicion=None,
            porcentaje=Decimal('5.00'),
            detalle='Retencion plataforma (5%)',
        )

        # Registrar premios globales individuales que correspondan a esta liga
        for p in premios_individuales:
            if p['liga_id'] == liga_id:
                HistorialGanador.objects.create(
                    fk_id_usuario=p['usuario_id'],
                    fk_id_liga=liga_id,
                    monto_pagado=p['monto_premio'],
                    tipo_premio='Global_Individual',
                    posicion=p['posicion'],
                    porcentaje=p['porcentaje_del_global'],
                    detalle=p['detalle'],
                )
                total_premio_liga += p['monto_premio']

        # Registrar premios globales por liga que correspondan a esta liga
        for p in premios_liga:
            if p['liga_id'] == liga_id:
                HistorialGanador.objects.create(
                    fk_id_usuario=p['usuario_id'],
                    fk_id_liga=liga_id,
                    monto_pagado=p['monto_premio'],
                    tipo_premio='Global_Liga',
                    posicion=None,
                    porcentaje=p['porcentaje_del_global'],
                    detalle=p['detalle'],
                )
                total_premio_liga += p['monto_premio']

        # Guardar resumen total del premio entregado en tabla premio
        Premio.objects.create(
            fk_id_liga=liga_id,
            monto_premio=total_premio_liga,
        )

        # Marcar liga como cerrada
        liga.estado = 'Cerrada'
        liga.save(update_fields=['estado'])

        return {
            'mensaje': 'Liga cerrada exitosamente',
            'liga_id': liga_id,
            'nombre_liga': liga.nombre_liga,
            'premios_locales': resumen_local,
            'premios_globales': resumen_global,
        }


# --- Funciones legacy mantenidas para compatibilidad ---

def inicializar_premios_liga(liga_id, distribucion=None):
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
    monto_total = Decimal(str(monto_total))
    porcentaje = Decimal(str(porcentaje))
    return (monto_total * porcentaje) / Decimal('100')


def obtener_distribucion_premios_liga(liga_id):
    premios = Premio.objects.filter(fk_id_liga=liga_id)
    if not premios.exists():
        inicializar_premios_liga(liga_id)
        premios = Premio.objects.filter(fk_id_liga=liga_id)
    return {p.posicion: p.porcentaje_premio for p in premios}


def calcular_premios_liga(liga_id):
    """Version legacy sin reglas de empate (usar calcular_premios_locales_con_empates)."""
    try:
        liga = Liga.objects.get(id_liga=liga_id)
    except Liga.DoesNotExist:
        return {'error': f'La liga {liga_id} no existe'}
    monto_total = liga.monto_total_recaudado or Decimal('0')
    if monto_total <= 0:
        return {'liga_id': liga_id, 'nombre_liga': liga.nombre_liga, 'monto_total': monto_total, 'error': 'No hay monto recaudado'}
    distribucion = obtener_distribucion_premios_liga(liga_id)
    ranking = obtener_ranking_con_posicion(liga_id)
    if not ranking:
        return {'liga_id': liga_id, 'nombre_liga': liga.nombre_liga, 'monto_total': monto_total, 'error': 'No hay participantes'}
    premios_calculados = []
    total_participantes = len(ranking)
    for posicion_data in ranking:
        posicion = posicion_data['posicion']
        usuario_id = posicion_data['usuario_id']
        puntos = posicion_data['puntos']
        porcentaje = None
        if posicion in distribucion:
            porcentaje = distribucion[posicion]
        elif posicion == total_participantes and -1 in distribucion:
            porcentaje = distribucion[-1]
        if porcentaje:
            monto_premio = calcular_monto_premio(monto_total, porcentaje)
            premios_calculados.append({'posicion': posicion, 'usuario_id': usuario_id, 'puntos': puntos, 'porcentaje': float(porcentaje), 'monto_premio': float(monto_premio)})
    total_distribuido = sum(p['monto_premio'] for p in premios_calculados)
    remanente = float(monto_total) - total_distribuido
    return {'liga_id': liga_id, 'nombre_liga': liga.nombre_liga, 'monto_total_recaudado': float(monto_total), 'total_participantes': total_participantes, 'premios': premios_calculados, 'total_distribuido': total_distribuido, 'remanente': remanente}


def obtener_premio_usuario(liga_id, usuario_id):
    resultado = calcular_premios_liga(liga_id)
    if 'error' in resultado:
        return resultado
    for premio in resultado.get('premios', []):
        if premio['usuario_id'] == usuario_id:
            return {'liga_id': liga_id, 'usuario_id': usuario_id, 'posicion': premio['posicion'], 'puntos': premio['puntos'], 'porcentaje': premio['porcentaje'], 'monto_premio': premio['monto_premio'], 'monto_total_liga': resultado['monto_total_recaudado']}
    return {'liga_id': liga_id, 'usuario_id': usuario_id, 'mensaje': 'No tienes premio en esta liga', 'posicion': None, 'monto_premio': 0}


def actualizar_distribucion_premios(liga_id, nueva_distribucion):
    premios_actualizados = []
    Premio.objects.filter(fk_id_liga=liga_id).delete()
    for posicion, porcentaje in nueva_distribucion.items():
        premio = Premio.objects.create(fk_id_liga=liga_id, posicion=posicion, porcentaje_premio=Decimal(str(porcentaje)))
        premios_actualizados.append(premio)
    return premios_actualizados
