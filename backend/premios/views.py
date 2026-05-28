from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Premio
from .serializers import (
    PremioSerializer,
    DistribucionPremiosSerializer,
    PremioUsuarioSerializer,
    ConfiguracionPremioSerializer
)
from .services import (
    calcular_premios_liga,
    obtener_premio_usuario,
    obtener_distribucion_premios_liga,
    actualizar_distribucion_premios,
    inicializar_premios_liga,
    DISTRIBUCION_DEFAULT,
    cerrar_liga,
    calcular_premios_locales_con_empates,
    calcular_premios_globales,
)


class PremioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar la configuración de premios.
    Permite CRUD completo de la tabla premio.
    """
    queryset = Premio.objects.all()
    serializer_class = PremioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar premios por liga"""
        queryset = super().get_queryset()
        liga_id = self.request.query_params.get('liga_id')
        
        if liga_id:
            try:
                liga_id = int(liga_id)
                queryset = queryset.filter(fk_id_liga=liga_id)
            except ValueError:
                return queryset.none()
            
        return queryset.order_by('posicion')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def premios_liga(request):
    """
    Obtiene la distribución de premios calculada para una liga.
    Muestra quién ganó qué según el ranking actual.
    
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
    
    resultado = calcular_premios_liga(liga_id_int)
    
    if 'error' in resultado:
        return Response(resultado, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(resultado)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mi_premio(request):
    """
    Obtiene el premio del usuario autenticado en una liga específica.
    
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
    
    usuario_id = request.user.id_usuario
    resultado = obtener_premio_usuario(liga_id_int, usuario_id)
    
    return Response(resultado)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def distribucion_liga(request):
    """
    Obtiene la configuración de distribución de premios de una liga.
    
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
    
    distribucion = obtener_distribucion_premios_liga(liga_id_int)
    
    return Response({
        'liga_id': liga_id_int,
        'distribucion': distribucion,
        'descripcion': {
            1: 'Primer lugar',
            2: 'Segundo lugar',
            3: 'Tercer lugar',
            -1: 'Último lugar'
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def configurar_premios(request):
    """
    Configura la distribución de premios para una liga.
    Solo administradores.
    
    Body params:
        liga_id: ID de la liga
        distribucion: Lista de {posicion, porcentaje}
        
    Ejemplo:
    {
        "liga_id": 1,
        "distribucion": [
            {"posicion": 1, "porcentaje": 50.00},
            {"posicion": 2, "porcentaje": 25.00},
            {"posicion": 3, "porcentaje": 10.00},
            {"posicion": -1, "porcentaje": 10.00}
        ]
    }
    """
    liga_id = request.data.get('liga_id')
    distribucion_data = request.data.get('distribucion')
    
    if not liga_id or not distribucion_data:
        return Response(
            {'error': 'Se requieren liga_id y distribucion'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validar que la suma de porcentajes no exceda 100%
    total_porcentaje = sum(item['porcentaje'] for item in distribucion_data)
    if total_porcentaje > 100:
        return Response(
            {'error': f'La suma de porcentajes ({total_porcentaje}%) no puede exceder 100%'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Convertir a formato de diccionario
        nueva_distribucion = {
            item['posicion']: item['porcentaje'] for item in distribucion_data
        }
        
        premios = actualizar_distribucion_premios(liga_id_int, nueva_distribucion)
        
        return Response({
            'mensaje': 'Distribución de premios actualizada correctamente',
            'liga_id': liga_id_int,
            'total_posiciones': len(premios),
            'suma_porcentajes': float(total_porcentaje)
        })
    except Exception as e:
        return Response(
            {'error': f'Error al configurar premios: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def inicializar_premios_default(request):
    """
    Inicializa la distribución de premios por defecto para una liga.
    Distribución: 50% (1°), 25% (2°), 10% (3°), 10% (último)
    
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
        premios = inicializar_premios_liga(liga_id_int)
        
        return Response({
            'mensaje': 'Premios inicializados con distribución por defecto',
            'liga_id': liga_id,
            'distribucion': {
                '1er_lugar': '50%',
                '2do_lugar': '25%',
                '3er_lugar': '10%',
                'ultimo_lugar': '10%'
            },
            'premios_creados': len(premios)
        })
    except Exception as e:
        return Response(
            {'error': f'Error al inicializar premios: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def premio_usuario_liga(request):
    """
    Obtiene el premio de un usuario específico en una liga.
    
    Query params:
        liga_id: ID de la liga
        usuario_id: ID del usuario
    """
    liga_id = request.query_params.get('liga_id')
    usuario_id = request.query_params.get('usuario_id')
    
    if not liga_id or not usuario_id:
        return Response(
            {'error': 'Se requieren los IDs de la liga y del usuario'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        liga_id_int = int(liga_id)
        usuario_id_int = int(usuario_id)
    except ValueError:
        return Response(
            {'error': 'Los IDs deben ser numéricos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    resultado = obtener_premio_usuario(liga_id_int, usuario_id_int)
    
    return Response(resultado)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def ejecutar_cierre_liga(request):
    """
    Ejecuta el cierre completo de una liga con distribucion de premios.
    Incluye premios locales (con reglas de empate), retencion de plataforma (5%)
    y premios globales (1% del total de todas las ligas).

    Body params:
        liga_id: ID de la liga a cerrar
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

    resultado = cerrar_liga(liga_id_int)

    if 'error' in resultado:
        return Response(resultado, status=status.HTTP_400_BAD_REQUEST)

    return Response(resultado, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def simular_cierre_liga(request):
    """
    Simula el cierre de una liga SIN persistir los premios.
    Util para ver la distribucion antes de cerrar oficialmente.

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

    premios_locales, resumen_local = calcular_premios_locales_con_empates(liga_id_int)

    if premios_locales is None:
        return Response(resumen_local, status=status.HTTP_400_BAD_REQUEST)

    premios_individuales, premios_liga, resumen_global = calcular_premios_globales()

    # Filtrar solo los premios globales que afectan a esta liga
    premios_globales_esta_liga = [p for p in premios_individuales if p['liga_id'] == liga_id_int]
    premios_globales_liga_esta = [p for p in premios_liga if p['liga_id'] == liga_id_int]

    return Response({
        'liga_id': liga_id_int,
        'premios_locales': resumen_local,
        'premios_globales_individuales': [
            {k: float(v) if hasattr(v, 'quantize') else v for k, v in p.items()}
            for p in premios_globales_esta_liga
        ],
        'premios_globales_liga': [
            {k: float(v) if hasattr(v, 'quantize') else v for k, v in p.items()}
            for p in premios_globales_liga_esta
        ],
        'resumen_global': resumen_global,
        'nota': 'Esta es una simulacion. No se han guardado los premios.',
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def premios_globales(request):
    """
    Obtiene el calculo de premios globales sobre todas las ligas de apuesta.
    """
    premios_individuales, premios_liga, resumen = calcular_premios_globales()

    if 'error' in resumen:
        return Response(resumen, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'premios_individuales': [
            {k: float(v) if hasattr(v, 'quantize') else v for k, v in p.items()}
            for p in premios_individuales
        ],
        'premios_por_liga': [
            {k: float(v) if hasattr(v, 'quantize') else v for k, v in p.items()}
            for p in premios_liga
        ],
        'resumen': resumen,
    })
