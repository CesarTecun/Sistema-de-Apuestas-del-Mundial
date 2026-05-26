from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.utils.permissions import EsAdministrador
from backend.utils.bitacora import registrar_bitacora
from .models import Usuario
from .serializers import AdminUsuarioSerializer


class AdminUsuarioViewSet(ModelViewSet):
    """Gestión de usuarios para el panel de administración (M7)."""
    serializer_class = AdminUsuarioSerializer
    permission_classes = [EsAdministrador]
    lookup_field = 'id_usuario'
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = Usuario.all_objects.all()
        rol = self.request.query_params.get('fk_rol')
        activo = self.request.query_params.get('activo')
        search = self.request.query_params.get('search')

        if rol:
            qs = qs.filter(fk_rol=rol)
        if activo is not None:
            qs = qs.filter(status=activo.lower() == 'true')
        if search:
            qs = qs.filter(
                Q(email__icontains=search) |
                Q(primer_nombre__icontains=search) |
                Q(primer_apellido__icontains=search)
            )
        return qs.order_by('id_usuario')

    @action(detail=True, methods=['post'])
    def activar(self, request, id_usuario=None):
        usuario = self.get_object()
        usuario.status = True
        usuario.deleted_at = None
        usuario.save(update_fields=['status', 'deleted_at'])
        registrar_bitacora(
            request.user.id_usuario,
            f'Admin activó usuario: {usuario.email} (id={usuario.id_usuario})'
        )
        return Response({
            'message': 'Usuario activado correctamente',
            'id_usuario': usuario.id_usuario,
        })

    @action(detail=True, methods=['post'])
    def desactivar(self, request, id_usuario=None):  # noqa: ARG002
        usuario = self.get_object()
        if usuario.id_usuario == request.user.id_usuario:
            return Response(
                {'error': 'No puedes desactivar tu propia cuenta'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        usuario.delete()
        registrar_bitacora(
            request.user.id_usuario,
            f'Admin desactivó usuario: {usuario.email} (id={usuario.id_usuario})'
        )
        return Response({
            'message': 'Usuario desactivado correctamente',
            'id_usuario': usuario.id_usuario,
        })
