from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Partido
from .serializers import PartidoSerializer

class PartidoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar partidos
    Permite operaciones CRUD completas
    """
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar partidos por liga si se especifica"""
        queryset = super().get_queryset()
        liga_id = self.request.query_params.get('liga_id')
        if liga_id:
            # Por ahora filtramos directamente, luego podemos agregar la relación con fases
            queryset = queryset.filter(fk_id_fase__isnull=False)
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Crear un nuevo partido"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        """Obtener un partido específico"""
        try:
            partido = self.get_object()
            serializer = self.get_serializer(partido)
            return Response(serializer.data)
        except Partido.DoesNotExist:
            return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Actualizar un partido existente"""
        try:
            partido = self.get_object()
            serializer = self.get_serializer(partido, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Partido.DoesNotExist:
            return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        """Eliminar un partido"""
        try:
            partido = self.get_object()
            partido.delete()
            return Response({'message': 'Partido eliminado correctamente'}, status=status.HTTP_200_OK)
        except Partido.DoesNotExist:
            return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def partidos_por_liga(request):
    """Obtener partidos de una liga específica"""
    liga_id = request.query_params.get('liga_id')
    if not liga_id:
        return Response({'error': 'Se requiere el ID de la liga'}, status=status.HTTP_400_BAD_REQUEST)
    
    partidos = Partido.objects.filter(fk_id_fase__isnull=False)
    serializer = PartidoSerializer(partidos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def partidos_por_equipo(request):
    """Obtener partidos de un equipo específico"""
    equipo_id = request.query_params.get('equipo_id')
    if not equipo_id:
        return Response({'error': 'Se requiere el ID del equipo'}, status=status.HTTP_400_BAD_REQUEST)
    
    partidos = Partido.objects.filter(
        Q(equipo_local=equipo_id) | Q(equipo_visitante=equipo_id)
    ).order_by('horario')
    serializer = PartidoSerializer(partidos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def actualizar_resultado(request, pk):
    """Actualizar resultado de un partido"""
    try:
        partido = Partido.objects.get(pk=pk)
        gol_local = request.data.get('gol_local')
        gol_visitante = request.data.get('gol_visitante')
        resultado = request.data.get('resultado')
        
        if gol_local is not None:
            partido.gol_local = gol_local
        if gol_visitante is not None:
            partido.gol_visitante = gol_visitante
        if resultado is not None:
            partido.resultado = resultado
            
        partido.save()
        
        serializer = PartidoSerializer(partido)
        return Response(serializer.data)
    except Partido.DoesNotExist:
        return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
