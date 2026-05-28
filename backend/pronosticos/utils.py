"""Utilidades para el módulo de pronósticos."""

from backend.posiciones.models import Ranking


def calcular_puntos_pronostico(gol_local_pred, gol_visitante_pred, gol_local_real, gol_visitante_real):
    """
    Calcula puntos comparando un pronóstico con el resultado real.

    Reglas:
    - 3 puntos: marcador exacto
    - 1 punto:  resultado correcto (ganador/empate) sin marcador exacto
    - 0 puntos: resultado incorrecto
    """
    if gol_local_real is None or gol_visitante_real is None:
        return 0

    # Marcador exacto
    if gol_local_pred == gol_local_real and gol_visitante_pred == gol_visitante_real:
        return 3

    # Resultado correcto
    pred_resultado = 'local' if gol_local_pred > gol_visitante_pred else ('visitante' if gol_visitante_pred > gol_local_pred else 'empate')
    real_resultado = 'local' if gol_local_real > gol_visitante_real else ('visitante' if gol_visitante_real > gol_local_real else 'empate')

    if pred_resultado == real_resultado:
        return 1

    return 0


def actualizar_ranking_por_liga(fk_id_usuario, fk_id_liga, puntos_nuevos):
    """Actualiza (o crea) el registro de ranking sumando los puntos nuevos."""
    ranking, _ = Ranking.objects.get_or_create(
        fk_id_usuario=fk_id_usuario,
        fk_id_liga=fk_id_liga,
        defaults={'puntos': 0, 'pj': 0}
    )
    ranking.puntos += puntos_nuevos
    ranking.pj += 1
    ranking.save()
