from django.db import models

class Liga(models.Model):
    id_liga = models.AutoField(primary_key=True)
    nombre_liga = models.CharField(max_length=100)
    fk_administrador = models.IntegerField(null=True, blank=True)
    monto_total_recaudado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=50, null=True, blank=True)
    tipo_liga = models.CharField(max_length=50, default='Diversion')
    
    class Meta:
        db_table = 'liga'
        managed = False  # Django no gestionará esta tabla (ya existe)
    
    def __str__(self):
        return self.nombre_liga


class PartidoLiga(models.Model):
    """
    Modelo para la tabla partido_liga.
    Relaciona partidos con ligas (qué partidos están disponibles para apostar en cada liga).
    """
    fk_id_liga = models.IntegerField()
    fk_id_partido = models.IntegerField()

    class Meta:
        db_table = 'partido_liga'
        managed = False
        unique_together = ('fk_id_liga', 'fk_id_partido')

    def __str__(self):
        return f"Liga {self.fk_id_liga} - Partido {self.fk_id_partido}"
