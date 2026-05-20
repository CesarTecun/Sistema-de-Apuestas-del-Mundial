from django.db import models
from backend.utils.models import SoftDeleteModel


class HistorialGanador(SoftDeleteModel):
    """
    Modelo para la tabla historial_ganador que registra
    todos los ganadores de premios de todas las ligas.
    Soporta premios locales, globales individuales, globales por liga y plataforma.
    """
    TIPOS_PREMIO = [
        ('Local', 'Premio Local de Liga'),
        ('Global_Individual', 'Premio Global Individual'),
        ('Global_Liga', 'Premio Global por Liga'),
        ('Plataforma', 'Retencion Plataforma'),
    ]

    id_pago = models.AutoField(primary_key=True)
    fk_id_usuario = models.IntegerField(null=True, blank=True)
    fk_id_liga = models.IntegerField()
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_premio = models.DateTimeField(auto_now_add=True)
    tipo_premio = models.CharField(max_length=20, choices=TIPOS_PREMIO, default='Local')
    posicion = models.IntegerField(null=True, blank=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    detalle = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'historial_ganador'
        app_label = 'historialganador'

    def __str__(self):
        return f"Pago {self.id_pago}: Usuario {self.fk_id_usuario} - Liga {self.fk_id_liga} - Q{self.monto_pagado} ({self.tipo_premio})"
