from django.db import models
from django.core.exceptions import ValidationError
from backend.utils.models import SoftDeleteModel

class Pronostico(SoftDeleteModel):
    id_pronostico = models.AutoField(primary_key=True)
    fk_id_usuario = models.IntegerField()
    fk_id_partido = models.IntegerField()
    fk_id_liga = models.IntegerField()
    gol_local = models.IntegerField()
    gol_visitante = models.IntegerField()

    class Meta:
        db_table = 'pronostico'
        managed = False  # Django no gestionará esta tabla (ya existe)
        app_label = 'pronosticos'
        # Un usuario solo puede hacer un pronóstico por partido en una liga
        unique_together = [['fk_id_usuario', 'fk_id_partido', 'fk_id_liga']]

    def __str__(self):
        return f"Pronóstico {self.id_pronostico}: Usuario {self.fk_id_usuario} - Partido {self.fk_id_partido} ({self.gol_local}-{self.gol_visitante})"
    
    @property
    def resultado_display(self):
        """Retorna el resultado formateado"""
        return f"{self.gol_local} - {self.gol_visitante}"
    
    @property
    def ganador_pronostico(self):
        """Determina el ganador según el pronóstico"""
        if self.gol_local > self.gol_visitante:
            return 'local'
        elif self.gol_visitante > self.gol_local:
            return 'visitante'
        else:
            return 'empate'
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.gol_local < 0:
            raise ValidationError({'gol_local': 'Los goles del equipo local no pueden ser negativos'})
        if self.gol_visitante < 0:
            raise ValidationError({'gol_visitante': 'Los goles del equipo visitante no pueden ser negativos'})
        
        # Validar que el partido exista y pertenezca a la liga
        if self.fk_id_partido and self.fk_id_liga:
            try:
                from backend.partidos.models import Partido
                partido = Partido.objects.get(id_partido=self.fk_id_partido)
                # Aquí podríamos agregar la validación de que el partido pertenezca a la liga
                # cuando tengamos la relación entre partidos y ligas
            except Partido.DoesNotExist:
                raise ValidationError({'fk_id_partido': 'El partido especificado no existe'})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
