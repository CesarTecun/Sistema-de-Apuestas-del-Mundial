from django.db import models
from django.utils import timezone
import json


class SoftDeleteManager(models.Manager):
    """
    Manager personalizado que por defecto solo retorna objetos activos (status=True).
    """
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class AllObjectsManager(models.Manager):
    """
    Manager que retorna todos los objetos incluyendo los eliminados lógicamente.
    """
    def get_queryset(self):
        return super().get_queryset()


class SoftDeleteModel(models.Model):
    """
    Modelo abstracto que implementa eliminación lógica (soft delete).
    Al llamar delete(), cambia status a False en lugar de eliminar físicamente.
    """
    status = models.BooleanField(default=True, db_column='status')
    deleted_at = models.DateTimeField(null=True, blank=True, db_column='deleted_at')

    # Manager por defecto: solo objetos activos
    objects = SoftDeleteManager()
    # Manager adicional: todos los objetos incluyendo eliminados
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Sobrescribe delete() para implementar soft delete.
        En lugar de eliminar el registro, cambia status a False.
        """
        self.status = False
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=['status', 'deleted_at'])

    def hard_delete(self, using=None, keep_parents=False, deleted_by=None):
        """
        Elimina físicamente el registro de la base de datos.
        Registra la eliminación en AuditLog si el modelo tiene la tabla correspondiente.
        Usar con precaución.
        """
        # Registrar en AuditLog antes de eliminar
        try:
            from backend.core.models import AuditLog
            table_name = self._meta.db_table
            pk_value = str(self.pk)

            # Obtener datos del objeto antes de eliminar
            old_data = {}
            for field in self._meta.fields:
                value = getattr(self, field.name)
                # Convertir datetime y otros objetos no serializables a string
                if hasattr(value, 'isoformat'):
                    old_data[field.name] = value.isoformat()
                else:
                    old_data[field.name] = value

            AuditLog.objects.create(
                table_name=table_name,
                operation='DELETE',
                record_pk=pk_value,
                old_data=old_data,
                new_data=None,
                changed_by=str(deleted_by) if deleted_by else 'unknown',
                changed_at=timezone.now()
            )
        except Exception as e:
            # Si falla el registro en AuditLog, continuar con la eliminación
            import traceback
            print(f"Error al registrar en AuditLog: {e}")
            traceback.print_exc()

        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """
        Restaura un registro eliminado lógicamente cambiando status a True.
        """
        self.status = True
        self.deleted_at = None
        self.save(update_fields=['status', 'deleted_at'])

    @property
    def is_deleted(self):
        """Retorna True si el registro fue eliminado lógicamente."""
        return self.deleted_at is not None
