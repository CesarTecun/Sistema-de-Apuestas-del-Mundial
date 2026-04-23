from django.db import models
from backend.utils.models import SoftDeleteModel


class Ranking(SoftDeleteModel):
    """
    Modelo para la tabla ranking que almacena las posiciones
    de los usuarios en cada liga.
    """
    id_registro = models.AutoField(primary_key=True)
    puntos = models.IntegerField(default=0)
    fk_id_usuario = models.IntegerField()
    fk_id_liga = models.IntegerField()
    pj = models.IntegerField(default=0)  # Partidos jugados (pronosticados)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'ranking'
        app_label = 'posiciones'

    def __str__(self):
        return f"Ranking {self.id_registro}: Usuario {self.fk_id_usuario} - Liga {self.fk_id_liga} - {self.puntos} pts"
