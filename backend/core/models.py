from django.db import models
from backend.utils.models import SoftDeleteModel


class AuditLog(models.Model):
    """Modelo para la tabla audit_log"""
    id_audit_log = models.BigAutoField(primary_key=True)
    table_name = models.CharField(max_length=100)
    operation = models.CharField(max_length=10)
    record_pk = models.TextField(null=True, blank=True)
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    changed_by = models.TextField(default='CURRENT_USER')
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_log'
        managed = False


class Bitacora(models.Model):
    """Modelo para la tabla bitacora"""
    log = models.AutoField(primary_key=True)
    hora = models.TimeField(auto_now_add=True)
    fecha = models.DateField(auto_now_add=True)
    detalle_accion = models.TextField()
    fk_id_usuario = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'bitacora'
        managed = False


class EquipoLiga(models.Model):
    """Modelo para la tabla equipoliga"""
    fk_id_liga = models.IntegerField()
    fk_id_seleccion = models.IntegerField()

    class Meta:
        db_table = 'equipoliga'
        managed = False
        unique_together = ('fk_id_liga', 'fk_id_seleccion')


class FaseGrupo(models.Model):
    """Modelo para la tabla fase_grupo"""
    id_fase = models.AutoField(primary_key=True)
    nombre_fase = models.CharField(max_length=50)

    class Meta:
        db_table = 'fase_grupo'
        managed = False


class Gol(models.Model):
    """Modelo para la tabla gol"""
    id_gol = models.AutoField(primary_key=True)
    fk_id_partido = models.IntegerField(null=True, blank=True)
    fk_id_jugador = models.IntegerField(null=True, blank=True)
    minuto_marcado = models.IntegerField()

    class Meta:
        db_table = 'gol'
        managed = False


class PartidoLiga(models.Model):
    """Modelo para la tabla partido_liga"""
    fk_id_liga = models.IntegerField()
    fk_id_partido = models.IntegerField()

    class Meta:
        db_table = 'partido_liga'
        managed = False
        unique_together = ('fk_id_liga', 'fk_id_partido')


class PosicionesTorneo(models.Model):
    """Modelo para la tabla posiciones_torneo"""
    id_posicion = models.AutoField(primary_key=True)
    fk_id_fase = models.IntegerField(null=True, blank=True)
    fk_id_seleccion = models.IntegerField(null=True, blank=True)
    pj = models.IntegerField(default=0)
    pg = models.IntegerField(default=0)
    pe = models.IntegerField(default=0)
    pp = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    gc = models.IntegerField(default=0)
    puntos = models.IntegerField(default=0)

    class Meta:
        db_table = 'posiciones_torneo'
        managed = False


class Premio(models.Model):
    """Modelo para la tabla premio"""
    id_premio = models.AutoField(primary_key=True)
    fk_id_liga = models.IntegerField(null=True, blank=True)
    posicion = models.IntegerField()
    porcentaje_premio = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'premio'
        managed = False


class Ranking(models.Model):
    """Modelo para la tabla ranking"""
    id_registro = models.AutoField(primary_key=True)
    puntos = models.IntegerField(default=0)
    fk_id_usuario = models.IntegerField(null=True, blank=True)
    fk_id_liga = models.IntegerField(null=True, blank=True)
    pj = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ranking'
        managed = False


class RolUsuario(models.Model):
    """Modelo para la tabla rol_usuario"""
    id_rol = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        db_table = 'rol_usuario'
        managed = False


class Sede(models.Model):
    """Modelo para la tabla sede"""
    id_sede = models.AutoField(primary_key=True)
    ciudad = models.CharField(max_length=100)
    estadio = models.CharField(max_length=100)

    class Meta:
        db_table = 'sede'
        managed = False


class SesionUsuario(models.Model):
    """Modelo para la tabla sesion_usuario"""
    id_sesion = models.AutoField(primary_key=True)
    fk_id_usuario = models.IntegerField()
    token_sesion = models.CharField(max_length=255, unique=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_ultima_actividad = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    estado_sesion = models.CharField(max_length=20, default='Activa')
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    dispositivo = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'sesion_usuario'
        managed = False
