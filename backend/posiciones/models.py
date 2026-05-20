from django.db import models
from backend.utils.models import SoftDeleteModel


class Ranking(SoftDeleteModel):
    """
    Modelo para la tabla ranking que almacena las posiciones
    de los usuarios en cada liga.
    """
    id_registro = models.AutoField(primary_key=True)
    puntos = models.IntegerField(default=0)
    fk_id_usuario = models.IntegerField(db_index=True)
    fk_id_liga = models.IntegerField(db_index=True)
    pj = models.IntegerField(default=0)  # Partidos jugados (pronosticados)
    posicion = models.IntegerField(null=True, blank=True)
    posicion_anterior = models.IntegerField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'ranking'
        app_label = 'posiciones'

    def __str__(self):
        return f"Ranking {self.id_registro}: Usuario {self.fk_id_usuario} - Liga {self.fk_id_liga} - {self.puntos} pts"


class HistorialRanking(models.Model):
    """
    Modelo para la tabla historial_ranking que registra
    snapshots de puntos por usuario/liga/jornada para calcular variación.
    """
    id_historial = models.AutoField(primary_key=True)
    fk_id_usuario = models.IntegerField(db_index=True)
    fk_id_liga = models.IntegerField(db_index=True)
    puntos = models.IntegerField(default=0)
    pj = models.IntegerField(default=0)
    posicion = models.IntegerField(null=True, blank=True)
    jornada = models.IntegerField(null=True, blank=True, db_index=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'historial_ranking'
        app_label = 'posiciones'

    def __str__(self):
        return f"Historial {self.id_historial}: Usuario {self.fk_id_usuario} - Liga {self.fk_id_liga} - J{self.jornada}: {self.puntos} pts"
