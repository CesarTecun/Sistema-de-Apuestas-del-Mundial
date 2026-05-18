from django.db import models
from django.utils import timezone


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

    def hard_delete(self, using=None, keep_parents=False):
        """
        Elimina físicamente el registro de la base de datos.
        Usar con precaución.
        """
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
