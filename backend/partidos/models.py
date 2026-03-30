from django.db import models

class Partido(models.Model):
    id_partido = models.AutoField(primary_key=True)
    horario = models.DateTimeField()
    equipo_local = models.IntegerField()
    equipo_visitante = models.IntegerField()
    fk_sede = models.IntegerField(null=True, blank=True)
    fk_id_fase = models.IntegerField(null=True, blank=True)
    gol_local = models.IntegerField(default=0)
    gol_visitante = models.IntegerField(default=0)
    ganador_penales = models.IntegerField(null=True, blank=True)
    tipo_partido = models.CharField(max_length=50, default='Regular')
    resultado = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'partido'
        managed = False  # Django no gestionará esta tabla (ya existe)
    
    def __str__(self):
        return f"Partido {self.id_partido}: {self.equipo_local} vs {self.equipo_visitante}"
    
    @property
    def resultado_display(self):
        """Retorna el resultado formateado"""
        if self.gol_local is not None and self.gol_visitante is not None:
            return f"{self.gol_local} - {self.gol_visitante}"
        return "Pendiente"
    
    @property
    def ganador(self):
        """Determina el ganador del partido"""
        if self.gol_local is not None and self.gol_visitante is not None:
            if self.gol_local > self.gol_visitante:
                return self.equipo_local
            elif self.gol_visitante > self.gol_local:
                return self.equipo_visitante
            elif self.ganador_penales is not None:
                return self.ganador_penales
        return None
