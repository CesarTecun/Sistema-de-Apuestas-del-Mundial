from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Pronostico
from .serializers import PronosticoSerializer

class PronosticoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar pronósticos
    Permite operaciones CRUD completas
    """
    queryset = Pronostico.objects.all()
    serializer_class = PronosticoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar pronósticos por usuario o liga"""
        queryset = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario_id')
        liga_id = self.request.query_params.get('liga_id')
        
        if usuario_id:
            queryset = queryset.filter(fk_id_usuario=usuario_id)
        if liga_id:
            queryset = queryset.filter(fk_id_liga=liga_id)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Crear un nuevo pronóstico"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verificar que el usuario no tenga ya un pronóstico para este partido en esta liga
        usuario_id = request.data.get('fk_id_usuario')
        partido_id = request.data.get('fk_id_partido')
        liga_id = request.data.get('fk_id_liga')
        
        if Pronostico.objects.filter(
            fk_id_usuario=usuario_id,
            fk_id_partido=partido_id,
            fk_id_liga=liga_id
        ).exists():
            return Response(
                {'error': 'Ya existe un pronóstico para este usuario en este partido y liga'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        """Obtener un pronóstico específico"""
        try:
            pronostico = self.get_object()
            serializer = self.get_serializer(pronostico)
            return Response(serializer.data)
        except Pronostico.DoesNotExist:
            return Response({'error': 'Pronóstico no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Actualizar un pronóstico existente"""
        try:
            pronostico = self.get_object()
            serializer = self.get_serializer(pronostico, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Pronostico.DoesNotExist:
            return Response({'error': 'Pronóstico no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        """Eliminar un pronóstico"""
        try:
            pronostico = self.get_object()
            pronostico.delete()
            return Response({'message': 'Pronóstico eliminado correctamente'}, status=status.HTTP_200_OK)
        except Pronostico.DoesNotExist:
            return Response({'error': 'Pronóstico no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pronosticos_por_usuario(request):
    """Obtener pronósticos de un usuario específico"""
    usuario_id = request.query_params.get('usuario_id')
    if not usuario_id:
        return Response({'error': 'Se requiere el ID del usuario'}, status=status.HTTP_400_BAD_REQUEST)
    
    pronosticos = Pronostico.objects.filter(fk_id_usuario=usuario_id)
    serializer = PronosticoSerializer(pronosticos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pronosticos_por_liga(request):
    """Obtener pronósticos de una liga específica"""
    liga_id = request.query_params.get('liga_id')
    if not liga_id:
        return Response({'error': 'Se requiere el ID de la liga'}, status=status.HTTP_400_BAD_REQUEST)
    
    pronosticos = Pronostico.objects.filter(fk_id_liga=liga_id)
    serializer = PronosticoSerializer(pronosticos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pronosticos_por_partido(request):
    """Obtener pronósticos de un partido específico"""
    partido_id = request.query_params.get('partido_id')
    if not partido_id:
        return Response({'error': 'Se requiere el ID del partido'}, status=status.HTTP_400_BAD_REQUEST)
    
    pronosticos = Pronostico.objects.filter(fk_id_partido=partido_id)
    serializer = PronosticoSerializer(pronosticos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pronosticos_usuario_liga(request):
    """Obtener pronósticos de un usuario en una liga específica"""
    usuario_id = request.query_params.get('usuario_id')
    liga_id = request.query_params.get('liga_id')
    
    if not usuario_id or not liga_id:
        return Response(
            {'error': 'Se requieren los IDs del usuario y la liga'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    pronosticos = Pronostico.objects.filter(
        fk_id_usuario=usuario_id,
        fk_id_liga=liga_id
    )
    serializer = PronosticoSerializer(pronosticos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verificar_pronostico_disponible(request):
    """Verificar si un usuario puede hacer un pronóstico para un partido en una liga"""
    usuario_id = request.data.get('usuario_id')
    partido_id = request.data.get('partido_id')
    liga_id = request.data.get('liga_id')
    
    if not all([usuario_id, partido_id, liga_id]):
        return Response(
            {'error': 'Se requieren los IDs del usuario, partido y liga'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    existe = Pronostico.objects.filter(
        fk_id_usuario=usuario_id,
        fk_id_partido=partido_id,
        fk_id_liga=liga_id
    ).exists()
    
    return Response({
        'disponible': not existe,
        'mensaje': 'Pronóstico disponible' if not existe else 'Ya existe un pronóstico para este partido'
    })
