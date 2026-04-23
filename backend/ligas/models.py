from django.db import models
from backend.utils.models import SoftDeleteModel

class Liga(SoftDeleteModel):
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


class ParticipanteLiga(SoftDeleteModel):
    """
    Modelo para la tabla participante_liga.
    Relaciona usuarios con ligas en las que participan.
    """
    id_participante = models.AutoField(primary_key=True)
    fk_id_liga = models.IntegerField()
    fk_id_usuario = models.IntegerField()
    fecha_union = models.DateTimeField(auto_now_add=True)
    estado_participacion = models.CharField(max_length=50, default='Activo')

    class Meta:
        db_table = 'participante_liga'
        managed = False
        unique_together = ('fk_id_liga', 'fk_id_usuario')

    def __str__(self):
        return f"Participante {self.id_participante}: Usuario {self.fk_id_usuario} en Liga {self.fk_id_liga}"


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


class Invitacion(models.Model):
    """
    Modelo para la tabla invitacion.
    Maneja invitaciones enviadas a usuarios para unirse a ligas.
    """
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
        ('Expirada', 'Expirada'),
    ]

    id_invitacion = models.AutoField(primary_key=True)
    fk_id_liga = models.IntegerField()
    fk_id_usuario_invitado = models.IntegerField()
    fk_id_usuario_administrador = models.IntegerField()
    fecha_invitacion = models.DateTimeField(auto_now_add=True)
    estado_invitacion = models.CharField(max_length=50, choices=ESTADOS, default='Pendiente')
    mensaje_invitacion = models.TextField(blank=True, null=True)
    email_invitado = models.EmailField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'invitacion'
        managed = False
        app_label = 'ligas'

    def __str__(self):
        return f"Invitación {self.id_invitacion} - Liga {self.fk_id_liga}"
