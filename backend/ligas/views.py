from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Liga
from .serializers import LigaSerializer

class LigaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar ligas
    Permite operaciones CRUD completas
    """
    queryset = Liga.objects.all()
    serializer_class = LigaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Crear una nueva liga"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        """Obtener una liga específica"""
        try:
            liga = self.get_object()
            serializer = self.get_serializer(liga)
            return Response(serializer.data)
        except Liga.DoesNotExist:
            return Response({'error': 'Liga no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Actualizar una liga existente"""
        try:
            liga = self.get_object()
            serializer = self.get_serializer(liga, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Liga.DoesNotExist:
            return Response({'error': 'Liga no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        """Eliminar una liga"""
        try:
            liga = self.get_object()
            liga.delete()
            return Response({'message': 'Liga eliminada correctamente'}, status=status.HTTP_200_OK)
        except Liga.DoesNotExist:
            return Response({'error': 'Liga no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ligas_por_usuario(request):
    """Obtener ligas administradas por un usuario específico"""
    usuario_id = request.query_params.get('usuario_id')
    if not usuario_id:
        return Response({'error': 'Se requiere el ID del usuario'}, status=status.HTTP_400_BAD_REQUEST)
    
    ligas = Liga.objects.filter(fk_administrador=usuario_id)
    serializer = LigaSerializer(ligas, many=True)
    return Response(serializer.data)
