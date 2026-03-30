from django.db import models
from django.contrib.auth.hashers import check_password, make_password


class UsuarioManager(models.Manager):
    """Manager personalizado para Usuario"""

    def get_by_natural_key(self, email):
        """Obtener usuario por email (requerido por Django auth)"""
        return self.get(email=email)


class Usuario(models.Model):
    """
    Modelo de usuario que mapea directamente la tabla public.usuario.
    No hereda de AbstractBaseUser para evitar campos adicionales de Django.
    """
    id_usuario = models.AutoField(primary_key=True)
    primer_nombre = models.CharField(max_length=50, blank=True, null=True)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=100)
    telefono = models.IntegerField(blank=True, null=True)
    contrasena = models.CharField(max_length=255)
    fk_rol = models.IntegerField(blank=True, null=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primer_nombre', 'primer_apellido']

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.email})"

    def check_password(self, raw_password):
        """Verifica la contraseña usando el hash de Django"""
        return check_password(raw_password, self.contrasena)

    def set_password(self, raw_password):
        """Genera hash de la contraseña"""
        self.contrasena = make_password(raw_password)

    @property
    def is_authenticated(self):
        """Siempre retorna True para usuarios de la BD"""
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        """Asumimos que todos los usuarios de la BD están activos"""
        return True

    @property
    def is_staff(self):
        """Admin si fk_rol = 1"""
        return self.fk_rol == 1

    @property
    def is_superuser(self):
        """Admin si fk_rol = 1"""
        return self.fk_rol == 1

    def get_username(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Retorna True si el usuario tiene el permiso"""
        return self.fk_rol == 1  # Admin tiene todos los permisos

    def has_module_perms(self, app_label):
        """Retorna True si el usuario tiene permisos para el app"""
        return self.fk_rol == 1  # Admin tiene acceso a todos los módulos

    def get_absolute_url(self):
        """URL absoluta del usuario"""
        return f"/api/auth/profile/{self.id_usuario}/"

    def get_full_name(self):
        """Retorna el nombre completo"""
        nombres = [self.primer_nombre, self.segundo_nombre]
        apellidos = [self.primer_apellido, self.segundo_apellido]
        nombre_completo = ' '.join(filter(None, nombres))
        apellido_completo = ' '.join(filter(None, apellidos))
        return f"{nombre_completo} {apellido_completo}".strip()

    def get_short_name(self):
        """Retorna el primer nombre"""
        return self.primer_nombre or self.email

    def natural_key(self):
        """Retorna la clave natural (email) para Django auth"""
        return (self.email,)


class RolUsuario(models.Model):
    """Modelo para la tabla de roles de usuario"""
    id_rol = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'rol_usuario'

    def __str__(self):
        return self.descripcion
