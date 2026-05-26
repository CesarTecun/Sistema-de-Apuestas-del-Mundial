from rest_framework.permissions import BasePermission


class EsAdministrador(BasePermission):
    """Permite acceso solo a usuarios con fk_rol = 1."""
    message = 'Se requiere rol de administrador para acceder a este recurso.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'fk_rol', None) == 1
        )
