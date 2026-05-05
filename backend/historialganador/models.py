from django.db import models
from backend.utils.models import SoftDeleteModel


class HistorialGanador(SoftDeleteModel):
    """
    Modelo para la tabla historial_ganador que registra
    todos los ganadores de premios de todas las ligas.
    Se comunica con ligas, premios y posiciones para
    almacenar el historial completo de ganadores.
    """
    id_pago = models.AutoField(primary_key=True)
    fk_id_usuario = models.IntegerField()
    fk_id_liga = models.IntegerField()
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_premio = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'historial_ganador'
        app_label = 'historialganador'

    def __str__(self):
        return f"Pago {self.id_pago}: Usuario {self.fk_id_usuario} - Liga {self.fk_id_liga} - Q{self.monto_pagado}"
