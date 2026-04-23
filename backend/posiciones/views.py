from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from backend.utils.viewsets import ReadOnlySoftDeleteModelViewSet
from .models import Ranking
from .serializers import (
    RankingSerializer,
    RankingConPosicionSerializer,
    PosicionUsuarioSerializer
)
from .services import (
    calcular_posicion_usuario,
    actualizar_ranking_usuario,
    calcular_todas_las_posiciones,
    obtener_ranking_con_posicion
)


class RankingViewSet(ReadOnlySoftDeleteModelViewSet):
    """
    API endpoint para consultar rankings.
    Solo lectura - las actualizaciones se hacen mediante los endpoints específicos.
    """
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar rankings por liga o usuario"""
        queryset = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario_id')
        liga_id = self.request.query_params.get('liga_id')
        
        if usuario_id:
            queryset = queryset.filter(fk_id_usuario=usuario_id)
        if liga_id:
            queryset = queryset.filter(fk_id_liga=liga_id)
            
        # Ordenar por puntos descendente
        return queryset.order_by('-puntos')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ranking_por_liga(request):
    """
    Obtiene el ranking completo de una liga con posiciones calculadas.
    
    Query params:
        liga_id: ID de la liga
    """
    liga_id = request.query_params.get('liga_id')
    if not liga_id:
        return Response(
            {'error': 'Se requiere el ID de la liga'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        ranking = obtener_ranking_con_posicion(liga_id)
        serializer = RankingConPosicionSerializer(ranking, many=True)
        return Response({
            'liga_id': liga_id,
            'total_participantes': len(ranking),
            'ranking': serializer.data
        })
    except Exception as e:
        return Response(
            {'error': f'Error al calcular ranking: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def posicion_usuario(request):
    """
    Obtiene la posición detallada de un usuario en una liga específica.
    
    Query params:
        usuario_id: ID del usuario
        liga_id: ID de la liga
    """
    usuario_id = request.query_params.get('usuario_id')
    liga_id = request.query_params.get('liga_id')
    
    if not usuario_id or not liga_id:
        return Response(
            {'error': 'Se requieren los IDs del usuario y la liga'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        datos = calcular_posicion_usuario(int(usuario_id), int(liga_id))
        serializer = PosicionUsuarioSerializer(datos)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Error al calcular posición: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def actualizar_ranking(request):
    """
    Actualiza el ranking de un usuario en una liga.
    Recalcula los puntos basándose en todos sus pronósticos.
    
    Body params:
        usuario_id: ID del usuario
        liga_id: ID de la liga
    """
    usuario_id = request.data.get('usuario_id')
    liga_id = request.data.get('liga_id')
    
    if not usuario_id or not liga_id:
        return Response(
            {'error': 'Se requieren los IDs del usuario y la liga'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        ranking = actualizar_ranking_usuario(int(usuario_id), int(liga_id))
        serializer = RankingSerializer(ranking)
        return Response({
            'mensaje': 'Ranking actualizado correctamente',
            'ranking': serializer.data
        })
    except Exception as e:
        return Response(
            {'error': f'Error al actualizar ranking: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def recalcular_ranking_liga(request):
    """
    Recalcula el ranking de TODOS los usuarios en una liga.
    
    Body params:
        liga_id: ID de la liga
    """
    liga_id = request.data.get('liga_id')
    
    if not liga_id:
        return Response(
            {'error': 'Se requiere el ID de la liga'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        rankings = calcular_todas_las_posiciones(int(liga_id))
        serializer = RankingSerializer(rankings, many=True)
        return Response({
            'mensaje': f'Ranking recalculado para {len(rankings)} usuarios',
            'total_usuarios': len(rankings),
            'ranking': serializer.data
        })
    except Exception as e:
        return Response(
            {'error': f'Error al recalcular ranking: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mi_ranking(request):
    """
    Obtiene el ranking del usuario autenticado en una liga específica.
    
    Query params:
        liga_id: ID de la liga
    """
    liga_id = request.query_params.get('liga_id')
    
    if not liga_id:
        return Response(
            {'error': 'Se requiere el ID de la liga'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtener el ID del usuario del token JWT
    usuario_id = request.user.id_usuario
    
    try:
        # Actualizar primero
        actualizar_ranking_usuario(usuario_id, int(liga_id))
        
        # Obtener el ranking completo para calcular la posición
        ranking_completo = obtener_ranking_con_posicion(int(liga_id))
        
        # Buscar la posición del usuario
        mi_posicion = None
        for item in ranking_completo:
            if item['usuario_id'] == usuario_id:
                mi_posicion = item
                break
        
        if mi_posicion:
            return Response({
                'mi_posicion': mi_posicion,
                'total_participantes': len(ranking_completo)
            })
        else:
            return Response(
                {'mensaje': 'No tienes pronósticos en esta liga'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {'error': f'Error al obtener ranking: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
