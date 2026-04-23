from django.db import models


class Premio(models.Model):
    """
    Modelo para la tabla premio que define la distribución
    de premios por posición en cada liga.
    """
    id_premio = models.AutoField(primary_key=True)
    fk_id_liga = models.IntegerField()
    posicion = models.IntegerField()
    porcentaje_premio = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'premio'
        app_label = 'premios'

    def __str__(self):
        return f"Premio Liga {self.fk_id_liga} - Posición {self.posicion}: {self.porcentaje_premio}%"
