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
        managed = True


class Bitacora(models.Model):
    """Modelo para la tabla bitacora"""
    log = models.AutoField(primary_key=True)
    hora = models.TimeField(auto_now_add=True)
    fecha = models.DateField(auto_now_add=True)
    detalle_accion = models.TextField()
    fk_id_usuario = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'bitacora'
        managed = True


class EquipoLiga(models.Model):
    """Modelo para la tabla equipoliga"""
    fk_id_liga = models.IntegerField()
    fk_id_seleccion = models.IntegerField()

    class Meta:
        db_table = 'equipoliga'
        managed = True
        unique_together = ('fk_id_liga', 'fk_id_seleccion')


class FaseGrupo(models.Model):
    """Modelo para la tabla fase_grupo"""
    id_fase = models.AutoField(primary_key=True)
    nombre_fase = models.CharField(max_length=50)

    class Meta:
        db_table = 'fase_grupo'
        managed = True


class Gol(models.Model):
    """Modelo para la tabla gol"""
    id_gol = models.AutoField(primary_key=True)
    fk_id_partido = models.IntegerField(null=True, blank=True)
    fk_id_jugador = models.IntegerField(null=True, blank=True)
    minuto_marcado = models.IntegerField()

    class Meta:
        db_table = 'gol'
        managed = True


class PosicionesTorneo(models.Model):
    """Modelo para la tabla posiciones_torneo — standings FIFA por liga."""
    id_posicion = models.AutoField(primary_key=True)
    fk_id_fase = models.IntegerField(null=True, blank=True)
    fk_id_seleccion = models.IntegerField(null=True, blank=True, db_index=True)
    fk_id_liga = models.IntegerField(null=True, blank=True, db_index=True)
    pj = models.IntegerField(default=0)
    pg = models.IntegerField(default=0)
    pe = models.IntegerField(default=0)
    pp = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    gc = models.IntegerField(default=0)
    dg = models.IntegerField(default=0)  # diferencia de gol: gf - gc
    puntos = models.IntegerField(default=0)
    posicion = models.IntegerField(null=True, blank=True)
    posicion_anterior = models.IntegerField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posiciones_torneo'
        managed = True
        unique_together = ('fk_id_liga', 'fk_id_seleccion')


class Sede(models.Model):
    """Modelo para la tabla sede"""
    id_sede = models.AutoField(primary_key=True)
    ciudad = models.CharField(max_length=100)
    estadio = models.CharField(max_length=100)

    class Meta:
        db_table = 'sede'
        managed = True


