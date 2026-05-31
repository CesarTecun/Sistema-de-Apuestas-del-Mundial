from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import json

from .models import Liga, ParticipanteLiga
from backend.core.models import AuditLog


@receiver(post_save, sender=Liga)
def log_liga_changes(sender, instance, created, **kwargs):
    """
    Registra cambios en la tabla liga en audit_log.
    Se ejecuta después de cada save() (INSERT y UPDATE).
    """
    try:
        # Obtener datos del objeto
        new_data = {}
        for field in instance._meta.fields:
            new_data[field.name] = getattr(instance, field.name)
        
        # Convertir datetime a string para JSON
        new_data_json = json.dumps(new_data, default=str)
        
        # Determinar la operación
        operation = 'INSERT' if created else 'UPDATE'
        
        # Para UPDATE, intentar obtener los datos anteriores
        old_data_json = None
        if not created:
            try:
                # Intentar obtener el estado anterior desde la base de datos
                old_instance = sender.objects.filter(pk=instance.pk).values()[0]
                old_data_json = json.dumps(old_instance, default=str)
            except Exception:
                # Si no se puede obtener el estado anterior, continuar sin old_data
                pass
        
        # Obtener el usuario que hizo el cambio
        changed_by = getattr(instance, 'updated_by', None) or getattr(instance, 'fk_administrador', None) or 'unknown'
        
        AuditLog.objects.create(
            table_name='liga',
            operation=operation,
            record_pk=str(instance.id_liga),
            old_data=old_data_json,
            new_data=new_data_json,
            changed_by=str(changed_by),
            changed_at=timezone.now()
        )
    except Exception as e:
        # Si falla el registro en AuditLog, no interrumpir la operación principal
        print(f"Error al registrar en AuditLog para Liga: {e}")


@receiver(post_delete, sender=Liga)
def log_liga_deletion(sender, instance, **kwargs):
    """
    Registra eliminaciones físicas de liga en audit_log.
    Se ejecuta después de un hard_delete().
    """
    try:
        # Obtener datos del objeto antes de eliminar
        old_data = {}
        for field in instance._meta.fields:
            old_data[field.name] = getattr(instance, field.name)
        
        # Convertir datetime a string para JSON
        old_data_json = json.dumps(old_data, default=str)
        
        # Obtener el usuario que eliminó
        changed_by = getattr(instance, 'deleted_by', None) or getattr(instance, 'updated_by', None) or 'unknown'
        
        AuditLog.objects.create(
            table_name='liga',
            operation='DELETE',
            record_pk=str(instance.id_liga),
            old_data=old_data_json,
            new_data=None,
            changed_by=str(changed_by),
            changed_at=timezone.now()
        )
    except Exception as e:
        # Si falla el registro en AuditLog, no interrumpir la operación principal
        print(f"Error al registrar eliminación de Liga en AuditLog: {e}")


@receiver(post_save, sender=ParticipanteLiga)
def log_participante_liga_changes(sender, instance, created, **kwargs):
    """
    Registra cambios en la tabla participante_liga en audit_log.
    También actualiza el monto total recaudado de la liga cuando un usuario se une.
    """
    try:
        # Obtener datos del objeto
        new_data = {}
        for field in instance._meta.fields:
            new_data[field.name] = getattr(instance, field.name)

        # Convertir datetime a string para JSON
        new_data_json = json.dumps(new_data, default=str)

        # Determinar la operación
        operation = 'INSERT' if created else 'UPDATE'

        # Para UPDATE, intentar obtener los datos anteriores
        old_data_json = None
        if not created:
            try:
                old_instance = sender.objects.filter(pk=instance.pk).values()[0]
                old_data_json = json.dumps(old_instance, default=str)
            except Exception:
                pass

        # Obtener el usuario que hizo el cambio
        changed_by = getattr(instance, 'updated_by', None) or getattr(instance, 'fk_id_usuario', None) or 'unknown'

        AuditLog.objects.create(
            table_name='participante_liga',
            operation=operation,
            record_pk=str(instance.id_participante),
            old_data=old_data_json,
            new_data=new_data_json,
            changed_by=str(changed_by),
            changed_at=timezone.now()
        )

        # Actualizar el monto total recaudado de la liga cuando un usuario se une
        if created and instance.estado_participacion == 'Activo':
            try:
                liga = Liga.objects.get(id_liga=instance.fk_id_liga)
                liga.actualizar_monto_total_recaudado()
            except Liga.DoesNotExist:
                pass
    except Exception as e:
        print(f"Error al registrar en AuditLog para ParticipanteLiga: {e}")


@receiver(post_delete, sender=ParticipanteLiga)
def log_participante_liga_deletion(sender, instance, **kwargs):
    """
    Registra eliminaciones físicas de participante_liga en audit_log.
    También actualiza el monto total recaudado de la liga cuando un usuario abandona.
    """
    try:
        # Obtener datos del objeto antes de eliminar
        old_data = {}
        for field in instance._meta.fields:
            old_data[field.name] = getattr(instance, field.name)

        # Convertir datetime a string para JSON
        old_data_json = json.dumps(old_data, default=str)

        # Obtener el usuario que eliminó
        changed_by = getattr(instance, 'deleted_by', None) or getattr(instance, 'updated_by', None) or 'unknown'

        AuditLog.objects.create(
            table_name='participante_liga',
            operation='DELETE',
            record_pk=str(instance.id_participante),
            old_data=old_data_json,
            new_data=None,
            changed_by=str(changed_by),
            changed_at=timezone.now()
        )

        # Actualizar el monto total recaudado de la liga cuando un usuario abandona
        try:
            liga = Liga.objects.get(id_liga=instance.fk_id_liga)
            liga.actualizar_monto_total_recaudado()
        except Liga.DoesNotExist:
            pass
    except Exception as e:
        print(f"Error al registrar eliminación de ParticipanteLiga en AuditLog: {e}")
