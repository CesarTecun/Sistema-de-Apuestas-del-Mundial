from django.db import models
from django.utils import timezone


class Premio(models.Model):
    """
    Modelo para la tabla premio que registra el premio total
    entregado al cerrar una liga.
    """
    id_premio = models.AutoField(primary_key=True)
    fk_id_liga = models.IntegerField()
    monto_premio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_premio = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'premio'
        app_label = 'premios'

    def __str__(self):
        return f"Premio {self.id_premio}: Liga {self.fk_id_liga} - Q{self.monto_premio}"
