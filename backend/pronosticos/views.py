import datetime

from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from backend.utils.viewsets import SoftDeleteModelViewSet
from backend.ligas.utils import obtener_ligas_usuario_ids
from backend.partidos.models import Partido
from .models import Pronostico
from .serializers import PronosticoSerializer
from .utils import calcular_puntos_pronostico, actualizar_ranking_por_liga


def _validar_ventana_pronostico(partido_id):
    """Valida que el partido aún permita pronósticos (15 min antes del inicio)."""
    try:
        partido = Partido.objects.get(id_partido=partido_id)
    except Partido.DoesNotExist:
        raise ValidationError({'fk_id_partido': 'El partido especificado no existe'})

    if partido.horario:
        cierre = partido.horario - datetime.timedelta(minutes=15)
        if timezone.now() >= cierre:
            raise ValidationError(
                {'detail': 'El registro de pronósticos para este partido ha cerrado (15 min antes del inicio).'}
            )
    return partido

class PronosticoViewSet(SoftDeleteModelViewSet):
    """
    API endpoint para gestionar pronósticos
    Permite operaciones CRUD completas
    """
    queryset = Pronostico.objects.all()
    serializer_class = PronosticoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar pronósticos al usuario autenticado y ligas permitidas (opcionalmente por liga/partido)."""
        usuario = self.request.user
        ligas_usuario = obtener_ligas_usuario_ids(usuario.id_usuario)
        queryset = Pronostico.objects.filter(
            fk_id_usuario=usuario.id_usuario,
            fk_id_liga__in=ligas_usuario
        )

        liga_id = self.request.query_params.get('liga_id')
        partido_id = self.request.query_params.get('partido_id')

        if liga_id:
            queryset = queryset.filter(fk_id_liga=liga_id)
        if partido_id:
            queryset = queryset.filter(fk_id_partido=partido_id)

        return queryset

    def perform_create(self, serializer):
        usuario_id = self.request.user.id_usuario
        liga_id = serializer.validated_data.get('fk_id_liga')
        partido_id = serializer.validated_data.get('fk_id_partido')

        if not liga_id or liga_id not in obtener_ligas_usuario_ids(usuario_id):
            raise PermissionDenied('No tienes permisos para pronosticar en esta liga.')

        if not Partido.objects.filter(id_partido=partido_id, fk_id_liga=liga_id).exists():
            raise ValidationError({'fk_id_partido': 'El partido no pertenece a la liga seleccionada.'})

        if Pronostico.objects.filter(
            fk_id_usuario=usuario_id,
            fk_id_partido=partido_id,
            fk_id_liga=liga_id
        ).exists():
            raise ValidationError({'detail': 'Ya registraste un pronóstico para este partido en esta liga.'})

        _validar_ventana_pronostico(partido_id)

        serializer.save(fk_id_usuario=usuario_id)

    def perform_update(self, serializer):
        pronostico = serializer.instance
        if pronostico.fk_id_usuario != self.request.user.id_usuario:
            raise PermissionDenied('Solo puedes editar tus propios pronósticos.')

        liga_id = pronostico.fk_id_liga
        if liga_id not in obtener_ligas_usuario_ids(self.request.user.id_usuario):
            raise PermissionDenied('No puedes modificar pronósticos de esta liga.')

        _validar_ventana_pronostico(pronostico.fk_id_partido)

        serializer.save()

    def perform_destroy(self, instance):
        if instance.fk_id_usuario != self.request.user.id_usuario:
            raise PermissionDenied('Solo puedes eliminar tus propios pronósticos.')
        if instance.fk_id_liga not in obtener_ligas_usuario_ids(self.request.user.id_usuario):
            raise PermissionDenied('No puedes eliminar pronósticos de esta liga.')
        instance.delete()
    
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
