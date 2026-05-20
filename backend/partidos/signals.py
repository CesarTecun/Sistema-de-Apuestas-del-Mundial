"""
Señales de Django para sincronizar automáticamente selecciones y partidos
con el microservicio marcador.
"""

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from backend.marcador_client import marcador_client, MarcadorClientError
from .models import Seleccion, Partido

logger = logging.getLogger(__name__)

# Flag para prevenir bucles de sincronización infinitos
_sync_from_webhook = False


def set_sync_from_webhook(value: bool):
    """Permite que el webhook del marcador desactive la señal de sincronización."""
    global _sync_from_webhook
    _sync_from_webhook = value


@receiver(post_save, sender=Seleccion)
def sync_seleccion_to_marcador(sender, instance, created, **kwargs):
    """
    Replica automáticamente cualquier creación o actualización de Seleccion
    al microservicio marcador usando codigo_iso como clave natural.
    """
    if not instance.codigo_iso:
        logger.warning(f"Seleccion {instance.id_seleccion} no tiene codigo_iso, omitiendo sincronización.")
        return

    payload = {
        "id_seleccion": instance.id_seleccion,
        "pais": instance.pais,
        "bandera": instance.bandera,
        "fk_id_fase_inicial": instance.fk_id_fase_inicial,
        "codigo_iso": instance.codigo_iso,
        "status": instance.status,
    }
    try:
        marcador_client.sync_seleccion(payload)
        logger.info(f"Seleccion {instance.id_seleccion} sincronizada con marcador.")
    except MarcadorClientError as exc:
        logger.error(f"Error sincronizando seleccion {instance.id_seleccion} con marcador: {exc}")


@receiver(post_save, sender=Partido)
def sync_partido_to_marcador(sender, instance, created, **kwargs):
    """
    Replica automáticamente cualquier creación o actualización de Partido
    al microservicio marcador usando el mismo id_partido.
    Omite la sincronización si el cambio provino del webhook del marcador
    para evitar bucles infinitos.
    """
    global _sync_from_webhook
    if _sync_from_webhook:
        return

    payload = {
        "id_partido": instance.id_partido,
        "horario": instance.horario.isoformat() if instance.horario else None,
        "equipo_local": instance.equipo_local,
        "equipo_visitante": instance.equipo_visitante,
        "fk_sede": instance.fk_sede,
        "fk_id_fase": instance.fk_id_fase,
        "fk_id_liga": instance.fk_id_liga,
        "gol_local": instance.gol_local,
        "gol_visitante": instance.gol_visitante,
        "ganador_penales": instance.ganador_penales,
        "tipo_partido": instance.tipo_partido,
        "resultado": instance.resultado,
        "estado": getattr(instance, "estado", "programado"),
        "status": instance.status,
    }
    try:
        marcador_client.sync_partido(payload)
        logger.info(f"Partido {instance.id_partido} sincronizado con marcador.")
    except MarcadorClientError as exc:
        logger.error(f"Error sincronizando partido {instance.id_partido} con marcador: {exc}")


@receiver(post_delete, sender=Partido)
def delete_partido_from_marcador(sender, instance, **kwargs):
    """
    Elimina el partido del microservicio marcador cuando se elimina físicamente de Django.
    Nota: Django usa soft delete por defecto, así que esto solo se dispara con hard_delete().
    """
    try:
        marcador_client.delete_partido_sync(instance.id_partido)
        logger.info(f"Partido {instance.id_partido} eliminado del marcador.")
    except MarcadorClientError as exc:
        logger.error(f"Error eliminando partido {instance.id_partido} del marcador: {exc}")


# ------------------------------------------------------------------
# Recálculo automático de standings y rankings al finalizar partido
# ------------------------------------------------------------------

@receiver(post_save, sender=Partido)
def recalcular_standings_y_rankings(sender, instance, created, **kwargs):
    """
    Cuando un partido finaliza (estado='finalizado'), recalcula:
    - Tabla de posiciones de equipos (FIFA-style) para la liga
    - Rankings de apostadores con posiciones y variaciones
    - Snapshot histórico del ranking
    """
    # Solo actuar cuando el partido tiene liga asignada y está finalizado
    if not instance.fk_id_liga or instance.estado_partido != 'finalizado':
        return

    liga_id = instance.fk_id_liga

    try:
        # 1) Recalcular tabla de equipos
        from backend.posiciones.services import recalcular_tabla_equipos
        recalcular_tabla_equipos(liga_id)
        logger.info(f"Tabla de equipos recalculada para liga {liga_id} tras partido {instance.id_partido}.")
    except Exception as exc:
        logger.error(f"Error recalculando tabla de equipos liga {liga_id}: {exc}")

    try:
        # 2) Recalcular rankings de apostadores y guardar posiciones anteriores
        from backend.posiciones.services import (
            calcular_todas_las_posiciones,
            actualizar_ranking_usuario,
            guardar_historial_ranking,
        )
        from backend.posiciones.models import Ranking
        from backend.pronosticos.models import Pronostico

        # Guardar posiciones actuales como "anteriores" antes de recalcular
        rankings_previos = {
            r.fk_id_usuario: r.posicion
            for r in Ranking.objects.filter(fk_id_liga=liga_id)
            if r.posicion is not None
        }

        # Obtener todos los usuarios que pronosticaron en esta liga
        usuarios_ids = Pronostico.objects.filter(
            fk_id_liga=liga_id
        ).values_list('fk_id_usuario', flat=True).distinct()

        rankings = []
        for usuario_id in usuarios_ids:
            ranking = actualizar_ranking_usuario(usuario_id, liga_id)
            rankings.append(ranking)

        # Ordenar y asignar posiciones
        rankings.sort(key=lambda x: x.puntos, reverse=True)

        posicion = 1
        puntos_anterior = None
        posicion_real = 1

        for r in rankings:
            if puntos_anterior is not None and r.puntos < puntos_anterior:
                posicion = posicion_real
            r.posicion_anterior = rankings_previos.get(r.fk_id_usuario)
            r.posicion = posicion
            r.save(update_fields=['posicion', 'posicion_anterior'])
            puntos_anterior = r.puntos
            posicion_real += 1

        logger.info(f"Rankings de apostadores recalculados para liga {liga_id}.")

        # 3) Guardar snapshot histórico
        guardar_historial_ranking(liga_id)

    except Exception as exc:
        logger.error(f"Error recalculando rankings liga {liga_id}: {exc}")
