"""
Señales de Django para actualizar automáticamente el ranking
cuando cambian los resultados de partidos o los pronósticos.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from backend.partidos.models import Partido
from backend.vaticinio.models import Pronostico
from .services import actualizar_ranking_usuario


@receiver(post_save, sender=Partido)
def actualizar_ranking_al_finalizar_partido(sender, instance, **kwargs):
    """
    Se ejecuta automáticamente cuando se guarda un partido.
    Si el partido tiene resultados (gol_local y gol_visitante),
    actualiza el ranking de todos los usuarios que hicieron pronósticos para este partido.
    """
    # Solo actualizar si el partido tiene resultados
    if instance.gol_local is not None and instance.gol_visitante is not None:
        # Buscar todos los pronósticos para este partido
        pronosticos = Pronostico.objects.filter(fk_id_partido=instance.id_partido)
        
        # Actualizar el ranking de cada usuario en cada liga
        ligas_actualizadas = set()
        for pronostico in pronosticos:
            actualizar_ranking_usuario(
                pronostico.fk_id_usuario, 
                pronostico.fk_id_liga
            )
            ligas_actualizadas.add(pronostico.fk_id_liga)
        
        if ligas_actualizadas:
            print(f"[Signal] Ranking actualizado para partido {instance.id_partido} en ligas: {ligas_actualizadas}")


@receiver(post_save, sender=Pronostico)
def actualizar_ranking_al_crear_pronostico(sender, instance, created, **kwargs):
    """
    Se ejecuta automáticamente cuando se crea o actualiza un pronóstico.
    Actualiza el ranking del usuario en la liga correspondiente.
    """
    actualizar_ranking_usuario(instance.fk_id_usuario, instance.fk_id_liga)
    print(f"[Signal] Ranking actualizado para usuario {instance.fk_id_usuario} en liga {instance.fk_id_liga}")


@receiver(post_delete, sender=Pronostico)
def actualizar_ranking_al_eliminar_pronostico(sender, instance, **kwargs):
    """
    Se ejecuta automáticamente cuando se elimina un pronóstico.
    Actualiza el ranking del usuario en la liga correspondiente.
    """
    actualizar_ranking_usuario(instance.fk_id_usuario, instance.fk_id_liga)
    print(f"[Signal] Ranking actualizado tras eliminar pronóstico de usuario {instance.fk_id_usuario}")
