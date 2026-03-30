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
