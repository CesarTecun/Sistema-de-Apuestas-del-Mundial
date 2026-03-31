"""
Señales de Django para guardar automáticamente los ganadores
en el historial cuando se distribuyen premios.

Se comunica con: ligas, premios y posiciones
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from backend.ligas.models import Liga
from backend.premios.models import Premio
from backend.posiciones.models import Ranking
from .models import HistorialGanador
from decimal import Decimal


# Estados que indican que la liga ha finalizado
ESTADOS_LIGA_FINALIZADA = ['Finalizada', 'Terminada', 'Cerrada', 'Completada']


def calcular_ganador_liga(liga_id):
    """
    Calcula los ganadores de una liga basándose en el ranking.
    Retorna los 4 principales: 1°, 2°, 3° y último lugar.
    """
    from backend.posiciones.services import obtener_ranking_con_posicion
    from backend.ligas.models import Liga
    
    try:
        liga = Liga.objects.get(id_liga=liga_id)
        ranking = obtener_ranking_con_posicion(liga_id)
        
        if not ranking:
            return []
        
        total_participantes = len(ranking)
        monto_total = liga.monto_total_recaudado or Decimal('0')
        
        # Distribución por defecto: 50%, 25%, 10%, 10%
        distribucion = {
            1: Decimal('50.00'),
            2: Decimal('25.00'),
            3: Decimal('10.00'),
        }
        # Último lugar si hay 4 o más participantes
        if total_participantes >= 4:
            distribucion[-1] = Decimal('10.00')  # -1 representa último
        
        ganadores = []
        for posicion_data in ranking:
            posicion = posicion_data['posicion']
            usuario_id = posicion_data['usuario_id']
            
            porcentaje = None
            if posicion in distribucion:
                porcentaje = distribucion[posicion]
            elif posicion == total_participantes and -1 in distribucion:
                porcentaje = distribucion[-1]
            
            if porcentaje:
                monto_premio = (monto_total * porcentaje) / Decimal('100')
                ganadores.append({
                    'usuario_id': usuario_id,
                    'posicion': posicion,
                    'monto_premio': monto_premio
                })
        
        return ganadores
        
    except Liga.DoesNotExist:
        return []


@receiver(post_save, sender=Liga)
def guardar_ganadores_al_finalizar_liga(sender, instance, created, **kwargs):
    """
    Se ejecuta automáticamente cuando se guarda una liga.
    Si el estado cambia a 'Finalizada' (o similar), calcula los ganadores
    y los guarda en el historial.
    """
    # Solo procesar si la liga ya existe (no es nueva)
    if created:
        return
    
    # Verificar si el estado indica que la liga finalizó
    estado_actual = instance.estado
    
    if not estado_actual or estado_actual.strip() not in ESTADOS_LIGA_FINALIZADA:
        return
    
    # Verificar si ya se registraron ganadores para esta liga
    ganadores_existentes = HistorialGanador.objects.filter(fk_id_liga=instance.id_liga).exists()
    
    if ganadores_existentes:
        print(f"[HistorialGanador] Los ganadores de la liga {instance.id_liga} ya están registrados.")
        return
    
    # Calcular ganadores
    ganadores = calcular_ganador_liga(instance.id_liga)
    
    if not ganadores:
        print(f"[HistorialGanador] No hay ganadores para registrar en la liga {instance.id_liga}.")
        return
    
    # Guardar en historial
    registrados = []
    for ganador in ganadores:
        try:
            historial = HistorialGanador.objects.create(
                fk_id_usuario=ganador['usuario_id'],
                fk_id_liga=instance.id_liga,
                monto_pagado=ganador['monto_premio']
            )
            registrados.append({
                'usuario_id': ganador['usuario_id'],
                'posicion': ganador['posicion'],
                'monto': float(ganador['monto_premio'])
            })
            print(f"[HistorialGanador] Guardado: Usuario {ganador['usuario_id']} - Posición {ganador['posicion']} - Q{ganador['monto_premio']}")
        except Exception as e:
            print(f"[HistorialGanador] Error al guardar ganador {ganador['usuario_id']}: {str(e)}")
    
    if registrados:
        print(f"[HistorialGanador] ¡{len(registrados)} ganadores registrados automáticamente para liga {instance.id_liga}!")
