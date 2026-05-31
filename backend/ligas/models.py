import uuid

from django.db import models
from django.db.models import Q
from backend.utils.models import SoftDeleteModel

class Liga(SoftDeleteModel):
    TIPOS_LIGA = [
        ('Diversion', 'Diversión'),
        ('Competitiva', 'Competitiva'),
    ]

    id_liga = models.AutoField(primary_key=True)
    nombre_liga = models.CharField(max_length=100)
    fk_administrador = models.IntegerField(null=True, blank=True, db_index=True)
    monto_total_recaudado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=50, null=True, blank=True)
    tipo_liga = models.CharField(max_length=50, choices=TIPOS_LIGA, default='Diversion')
    descripcion = models.TextField(blank=True)
    es_publica = models.BooleanField(
        default=False,
        help_text='Visible en el buscador público si está activa.'
    )
    cupo_maximo = models.PositiveIntegerField(blank=True, null=True)
    requiere_aprobacion = models.BooleanField(
        default=True,
        help_text='Si está activo, los administradores deben aprobar cada solicitud.'
    )
    # Campos de auditoría
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True, db_index=True)
    deleted_by = models.IntegerField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = 'liga'
        managed = True

    def __str__(self):
        return self.nombre_liga


class ParticipanteLiga(SoftDeleteModel):
    """
    Modelo para la tabla participante_liga.
    Relaciona usuarios con ligas en las que participan.
    """
    id_participante = models.AutoField(primary_key=True)
    fk_id_liga = models.IntegerField(db_index=True)
    fk_id_usuario = models.IntegerField(db_index=True)
    fecha_union = models.DateTimeField(auto_now_add=True)
    estado_participacion = models.CharField(max_length=50, default='Activo')
    # Campos de auditoría
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True, db_index=True)
    deleted_by = models.IntegerField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = 'participante_liga'
        managed = True
        unique_together = ('fk_id_liga', 'fk_id_usuario')

    def __str__(self):
        return f"Participante {self.id_participante}: Usuario {self.fk_id_usuario} en Liga {self.fk_id_liga}"


class PartidoLiga(models.Model):
    """
    Modelo para la tabla partido_liga.
    Relaciona partidos con ligas (qué partidos están disponibles para apostar en cada liga).
    """
    fk_id_liga = models.IntegerField(db_index=True)
    fk_id_partido = models.IntegerField(db_index=True)

    class Meta:
        db_table = 'partido_liga'
        managed = True
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
    codigo_invitacion = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    fk_id_usuario_invitado = models.IntegerField(null=True, blank=True, db_index=True)
    fk_id_usuario_administrador = models.IntegerField()
    fecha_invitacion = models.DateTimeField(auto_now_add=True)
    estado_invitacion = models.CharField(max_length=50, choices=ESTADOS, default='Pendiente')
    mensaje_invitacion = models.TextField(blank=True, null=True)
    email_invitado = models.EmailField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'invitacion'
        managed = True
        app_label = 'ligas'

    def __str__(self):
        return f"Invitación {self.id_invitacion} - Liga {self.fk_id_liga}"


class SolicitudParticipacion(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('Rechazada', 'Rechazada'),
    ]

    id_solicitud = models.AutoField(primary_key=True)
    liga = models.ForeignKey(
        Liga,
        on_delete=models.CASCADE,
        related_name='solicitudes'
    )
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitudes_participacion'
    )
    email_contacto = models.EmailField()
    mensaje = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Pendiente',
        db_index=True
    )
    respuesta_admin = models.TextField(blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    respondido_por = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'solicitud_participacion'
        ordering = ['-fecha_solicitud']
        constraints = [
            models.UniqueConstraint(
                fields=('liga', 'usuario'),
                condition=Q(estado='Pendiente') & Q(usuario__isnull=False),
                name='unique_solicitud_liga_usuario_pendiente'
            )
        ]

    def __str__(self):
        return f"Solicitud {self.id_solicitud} - Liga {self.liga_id}"
