from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum
from backend.utils.viewsets import ReadOnlySoftDeleteModelViewSet
from .models import HistorialGanador
from .serializers import HistorialGanadorSerializer, ResumenGanadorSerializer


class HistorialGanadorViewSet(ReadOnlySoftDeleteModelViewSet):
    """
    API endpoint para consultar el historial de ganadores.
    Solo lectura - los registros se crean automáticamente.
    """
    queryset = HistorialGanador.objects.all()
    serializer_class = HistorialGanadorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar historial por liga o usuario"""
        queryset = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario_id')
        liga_id = self.request.query_params.get('liga_id')
        
        if usuario_id:
            queryset = queryset.filter(fk_id_usuario=usuario_id)
        if liga_id:
            queryset = queryset.filter(fk_id_liga=liga_id)
            
        return queryset.order_by('-fecha_premio')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def historial_por_liga(request):
    """
    Obtiene el historial de ganadores de una liga específica.
    
    Query params:
        liga_id: ID de la liga
    """
    liga_id = request.query_params.get('liga_id')
    if not liga_id:
        return Response(
            {'error': 'Se requiere el ID de la liga'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    ganadores = HistorialGanador.objects.filter(fk_id_liga=liga_id)
    
    if not ganadores.exists():
        return Response({
            'liga_id': liga_id,
            'mensaje': 'No hay ganadores registrados para esta liga'
        })
    
    total_pagado = ganadores.aggregate(total=Sum('monto_pagado'))['total'] or 0
    
    serializer = HistorialGanadorSerializer(ganadores, many=True)
    
    return Response({
        'liga_id': int(liga_id),
        'total_ganadores': ganadores.count(),
        'monto_total_pagado': float(total_pagado),
        'ganadores': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mis_premios(request):
    """
    Obtiene el historial de premios del usuario autenticado.
    """
    usuario_id = request.user.id_usuario
    
    premios = HistorialGanador.objects.filter(fk_id_usuario=usuario_id)
    
    if not premios.exists():
        return Response({
            'usuario_id': usuario_id,
            'mensaje': 'No tienes premios registrados',
            'total_premios': 0,
            'monto_total': 0
        })
    
    total_ganado = premios.aggregate(total=Sum('monto_pagado'))['total'] or 0
    
    serializer = HistorialGanadorSerializer(premios, many=True)
    
    return Response({
        'usuario_id': usuario_id,
        'total_premios': premios.count(),
        'monto_total_ganado': float(total_ganado),
        'premios': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def resumen_historial(request):
    """
    Obtiene un resumen completo de todos los ganadores.
    Solo para administradores.
    """
    total_registros = HistorialGanador.objects.count()
    
    if total_registros == 0:
        return Response({
            'mensaje': 'No hay registros en el historial',
            'total_registros': 0
        })
    
    monto_total = HistorialGanador.objects.aggregate(total=Sum('monto_pagado'))['total'] or 0
    
    # Agrupar por liga
    ligas_con_ganadores = HistorialGanador.objects.values('fk_id_liga').distinct().count()
    
    return Response({
        'total_registros': total_registros,
        'total_ligas_con_ganadores': ligas_con_ganadores,
        'monto_total_distribuido': float(monto_total)
    })
