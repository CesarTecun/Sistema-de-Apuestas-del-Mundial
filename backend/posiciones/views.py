from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from backend.utils.viewsets import ReadOnlySoftDeleteModelViewSet
from .models import Ranking
from .serializers import (
    RankingSerializer,
    RankingConPosicionSerializer,
    PosicionUsuarioSerializer,
    TablaPosicionEquipoSerializer
)
from .services import (
    calcular_posicion_usuario,
    actualizar_ranking_usuario,
    calcular_todas_las_posiciones,
    obtener_ranking_con_posicion,
    obtener_tabla_equipos,
    recalcular_tabla_equipos
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
            try:
                usuario_id = int(usuario_id)
                queryset = queryset.filter(fk_id_usuario=usuario_id)
            except ValueError:
                return queryset.none()
        if liga_id:
            try:
                liga_id = int(liga_id)
                queryset = queryset.filter(fk_id_liga=liga_id)
            except ValueError:
                return queryset.none()
            
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
        liga_id_int = int(liga_id)
    except ValueError:
        return Response(
            {'error': 'liga_id debe ser numérico'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        ranking = obtener_ranking_con_posicion(liga_id_int)
        serializer = RankingConPosicionSerializer(ranking, many=True)
        return Response({
            'liga_id': liga_id_int,
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
        usuario_id_int = int(usuario_id)
        liga_id_int = int(liga_id)
    except ValueError:
        return Response(
            {'error': 'Los IDs deben ser numéricos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        datos = calcular_posicion_usuario(usuario_id_int, liga_id_int)
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
        usuario_id_int = int(usuario_id)
        liga_id_int = int(liga_id)
    except ValueError:
        return Response(
            {'error': 'Los IDs deben ser numéricos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        ranking = actualizar_ranking_usuario(usuario_id_int, liga_id_int)
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
        liga_id_int = int(liga_id)
    except ValueError:
        return Response(
            {'error': 'liga_id debe ser numérico'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        rankings = calcular_todas_las_posiciones(liga_id_int)
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
        liga_id_int = int(liga_id)
    except ValueError:
        return Response(
            {'error': 'liga_id debe ser numérico'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Actualizar primero
        actualizar_ranking_usuario(usuario_id, liga_id_int)
        
        # Obtener el ranking completo para calcular la posición
        ranking_completo = obtener_ranking_con_posicion(liga_id_int)
        
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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def tabla_equipos_por_liga(request):
    """
    Obtiene la tabla de posiciones FIFA-style de equipos para una liga.
    Incluye posición, variación (↑↓→), puntos, partidos, goles, etc.

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
        liga_id_int = int(liga_id)
    except ValueError:
        return Response(
            {'error': 'liga_id debe ser numérico'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        tabla = obtener_tabla_equipos(liga_id_int)
        if not tabla.exists():
            # Si no hay datos, recalcular desde los partidos finalizados
            recalcular_tabla_equipos(liga_id_int)
            tabla = obtener_tabla_equipos(liga_id_int)

        serializer = TablaPosicionEquipoSerializer(tabla, many=True)
        return Response({
            'liga_id': liga_id_int,
            'total_equipos': len(serializer.data),
            'tabla': serializer.data
        })
    except Exception as e:
        return Response(
            {'error': f'Error al obtener tabla de equipos: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
