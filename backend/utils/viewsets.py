from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet personalizado que implementa Soft Delete (eliminación lógica).
    
    - list: Solo muestra registros con status=True
    - retrieve: Solo permite ver registros con status=True
    - create: Crea registros con status=True por defecto
    - update/partial_update: Solo actualiza registros con status=True
    - destroy: Realiza soft delete (cambia status a False)
    - restore: Endpoint adicional para restaurar registros eliminados
    - hard_delete: Endpoint adicional para eliminar físicamente (con permisos)
    """
    
    def get_queryset(self):
        """
        Retorna solo registros activos (status=True).
        El manager por defecto ya filtra por status=True.
        """
        return self.queryset.model.objects.all()
    
    def get_object(self):
        """
        Obtiene un objeto solo si está activo (status=True).
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Realizar la búsqueda
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        
        assert lookup_url_kwarg in self.kwargs, (
            f'Expected view {self.__class__.__name__} to be called with a URL keyword argument '
            f'named "{lookup_url_kwarg}". Fix your URL conf, or set the `.lookup_field` '
            f'attribute on the view correctly.'
        )
        
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = queryset.filter(**filter_kwargs).first()
        
        if not obj:
            raise NotFound(detail="No encontrado o ha sido eliminado.")
        
        # Verificar permisos
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    def destroy(self, request, *args, **kwargs):
        """
        Realiza soft delete en lugar de eliminación física.
        Cambia status a False.
        """
        instance = self.get_object()
        instance.delete()  # Este delete() es el soft delete del modelo
        return Response(
            {'message': 'Registro eliminado correctamente (eliminación lógica)'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """
        Restaura un registro eliminado lógicamente.
        Cambia status de False a True.
        """
        try:
            # Usar all_objects para incluir eliminados
            instance = self.queryset.model.all_objects.get(pk=pk)
            
            if instance.status:
                return Response(
                    {'message': 'El registro ya está activo'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            instance.restore()
            serializer = self.get_serializer(instance)
            return Response({
                'message': 'Registro restaurado correctamente',
                'data': serializer.data
            })
        except self.queryset.model.DoesNotExist:
            raise NotFound(detail="Registro no encontrado.")
    
    @action(detail=False, methods=['get'])
    def deleted(self, request):
        """
        Lista todos los registros eliminados lógicamente.
        """
        queryset = self.queryset.model.all_objects.filter(status=False)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'], permission_classes=[])
    def hard_delete(self, request, pk=None):
        """
        Elimina físicamente un registro de la base de datos.
        ⚠️ Usar con precaución. Requiere permisos de administrador.
        """
        # Verificar si el usuario es administrador
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos para realizar esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            # Buscar en todos los objetos incluyendo eliminados
            instance = self.queryset.model.all_objects.get(pk=pk)
            instance.hard_delete()
            return Response(
                {'message': 'Registro eliminado físicamente de la base de datos'},
                status=status.HTTP_200_OK
            )
        except self.queryset.model.DoesNotExist:
            raise NotFound(detail="Registro no encontrado.")


class ReadOnlySoftDeleteModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet que solo muestra registros activos.
    Para modelos de solo lectura que usan soft delete.
    """
    
    def get_queryset(self):
        """Retorna solo registros activos (status=True)"""
        return self.queryset.model.objects.all()
