from django.db import models


class SesionUsuario(models.Model):
    """
    Modelo para la tabla sesion_usuario.
    Registra los inicios de sesion de usuarios y su estado activo.
    """
    ESTADOS = [
        ('Activa', 'Activa'),
        ('Cerrada', 'Cerrada'),
        ('Expirada', 'Expirada'),
    ]

    id_sesion = models.AutoField(primary_key=True)
    fk_id_usuario = models.IntegerField(db_index=True)
    token_sesion = models.CharField(max_length=255, unique=True, db_index=True)
    refresh_token_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    jwt_jti = models.CharField(max_length=50, null=True, blank=True, unique=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_ultima_actividad = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    estado_sesion = models.CharField(max_length=20, choices=ESTADOS, default='Activa')
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    dispositivo = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'sesion_usuario'
        app_label = 'autenticacion'

    def __str__(self):
        return f"Sesion {self.id_sesion} - Usuario {self.fk_id_usuario} ({self.estado_sesion})"

    @property
    def is_activa(self):
        return self.estado_sesion == 'Activa'

    def cerrar_sesion(self):
        from django.utils import timezone
        self.estado_sesion = 'Cerrada'
        self.fecha_cierre = timezone.now()
        self.save(update_fields=['estado_sesion', 'fecha_cierre'])

    def actualizar_actividad(self):
        from django.utils import timezone
        self.fecha_ultima_actividad = timezone.now()
        self.save(update_fields=['fecha_ultima_actividad'])


class PasswordResetToken(models.Model):
    """Tokens de recuperación de contraseña enviados por correo."""
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='password_reset_tokens'
    )
    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'password_reset_token'
        ordering = ['-created_at']

    @property
    def is_active(self):
        from django.utils import timezone
        return self.used_at is None and timezone.now() <= self.expires_at

    def mark_used(self):
        from django.utils import timezone
        self.used_at = timezone.now()
        self.save(update_fields=['used_at'])


class EmailVerificationToken(models.Model):
    """Tokens de verificación de email enviados al registrarse."""
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='email_verification_tokens'
    )
    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'email_verification_token'
        ordering = ['-created_at']

    @property
    def is_active(self):
        from django.utils import timezone
        return self.used_at is None and timezone.now() <= self.expires_at

    def mark_used(self):
        from django.utils import timezone
        self.used_at = timezone.now()
        self.save(update_fields=['used_at'])
