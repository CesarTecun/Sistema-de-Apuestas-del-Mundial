from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django.db.models import Q
from backend.utils.viewsets import SoftDeleteModelViewSet
from .models import Partido, Jugador, Seleccion
from .serializers import PartidoSerializer, JugadorSerializer, SeleccionSerializer
from backend.ligas.utils import (
    obtener_ligas_usuario_ids,
    obtener_ligas_administradas_ids,
)
from backend.pronosticos.models import Pronostico
from backend.pronosticos.utils import calcular_puntos_pronostico, actualizar_ranking_por_liga

class JugadorViewSet(SoftDeleteModelViewSet):
    """
    API endpoint para gestionar jugadores.
    Implementa soft delete - al "eliminar" solo cambia status a False.
    """
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id_jugador'


class SeleccionViewSet(SoftDeleteModelViewSet):
    """
    API endpoint para gestionar selecciones.
    Implementa soft delete - al "eliminar" solo cambia status a False.
    """
    queryset = Seleccion.objects.all()
    serializer_class = SeleccionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id_seleccion'


class PartidoViewSet(SoftDeleteModelViewSet):
    """
    API endpoint para gestionar partidos
    Permite operaciones CRUD completas
    """
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar partidos a las ligas permitidas y opcionalmente por liga específica."""
        ligas_usuario = obtener_ligas_usuario_ids(self.request.user.id_usuario)
        if not ligas_usuario:
            return Partido.objects.none()

        queryset = Partido.objects.filter(fk_id_liga__in=ligas_usuario)

        liga_id = self.request.query_params.get('liga_id')
        if liga_id:
            try:
                liga_id_int = int(liga_id)
            except ValueError:
                raise ValidationError({'liga_id': 'El identificador de liga debe ser numérico.'})

            if liga_id_int not in ligas_usuario:
                raise PermissionDenied('No tienes permisos para consultar esta liga.')

            queryset = queryset.filter(fk_id_liga=liga_id_int)

        return queryset
    
    def create(self, request, *args, **kwargs):
        """Crear un nuevo partido"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        """Obtener un partido específico"""
        try:
            partido = self.get_object()
            serializer = self.get_serializer(partido)
            return Response(serializer.data)
        except Partido.DoesNotExist:
            return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        liga_id = serializer.validated_data.get('fk_id_liga')
        self._validar_liga_administrada(liga_id)
        serializer.save()

    def perform_update(self, serializer):
        liga_id = serializer.validated_data.get('fk_id_liga', serializer.instance.fk_id_liga)
        self._validar_liga_administrada(liga_id)
        serializer.save()

    def _validar_liga_administrada(self, liga_id):
        if not liga_id:
            raise ValidationError({'fk_id_liga': 'Debes seleccionar la liga a la que pertenece el partido.'})
        ligas_admin = obtener_ligas_administradas_ids(self.request.user.id_usuario)
        if liga_id not in ligas_admin:
            raise PermissionDenied('Solo el administrador de la liga puede gestionar partidos.')
    
    def update(self, request, pk=None):
        """Actualizar un partido existente"""
        try:
            partido = self.get_object()
            serializer = self.get_serializer(partido, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Partido.DoesNotExist:
            return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        """Eliminar un partido"""
        try:
            partido = self.get_object()
            self._validar_liga_administrada(partido.fk_id_liga)
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
    
    try:
        liga_id_int = int(liga_id)
    except ValueError:
        return Response({'error': 'liga_id debe ser numérico'}, status=status.HTTP_400_BAD_REQUEST)

    ligas_usuario = obtener_ligas_usuario_ids(request.user.id_usuario)
    if liga_id_int not in ligas_usuario:
        raise PermissionDenied('No tienes permisos para consultar esta liga.')

    partidos = Partido.objects.filter(fk_id_liga=liga_id_int)
    serializer = PartidoSerializer(partidos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def partidos_por_equipo(request):
    """Obtener partidos de un equipo específico dentro de las ligas permitidas"""
    equipo_id = request.query_params.get('equipo_id')
    if not equipo_id:
        return Response({'error': 'Se requiere el ID del equipo'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        equipo_id_int = int(equipo_id)
    except ValueError:
        return Response({'error': 'equipo_id debe ser numérico'}, status=status.HTTP_400_BAD_REQUEST)

    ligas_usuario = obtener_ligas_usuario_ids(request.user.id_usuario)
    if not ligas_usuario:
        return Response([], status=status.HTTP_200_OK)

    partidos = Partido.objects.filter(
        Q(equipo_local=equipo_id_int) | Q(equipo_visitante=equipo_id_int)
    ).filter(fk_id_liga__in=ligas_usuario).order_by('horario')
    serializer = PartidoSerializer(partidos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def actualizar_resultado(request, pk):
    """Actualizar resultado de un partido"""
    try:
        partido = Partido.objects.get(pk=pk)
        ligas_admin = obtener_ligas_administradas_ids(request.user.id_usuario)
        if partido.fk_id_liga not in ligas_admin:
            raise PermissionDenied('Solo el administrador de la liga puede actualizar este partido.')

        gol_local = request.data.get('gol_local')
        gol_visitante = request.data.get('gol_visitante')
        resultado = request.data.get('resultado')

        if gol_local is not None:
            partido.gol_local = int(gol_local)
        if gol_visitante is not None:
            partido.gol_visitante = int(gol_visitante)
        if resultado is not None:
            partido.resultado = resultado

        partido.save()

        # Calcular puntos de pronósticos si ambos goles están definidos
        if partido.gol_local is not None and partido.gol_visitante is not None:
            pronosticos = Pronostico.objects.filter(fk_id_partido=partido.id_partido, status=True)
            for pronostico in pronosticos:
                puntos = calcular_puntos_pronostico(
                    pronostico.gol_local,
                    pronostico.gol_visitante,
                    partido.gol_local,
                    partido.gol_visitante,
                )
                # Solo actualizar si cambió el puntaje o si aún no fue calculado
                if pronostico.puntos_obtenidos != puntos:
                    diferencia = puntos - pronostico.puntos_obtenidos
                    pronostico.puntos_obtenidos = puntos
                    pronostico.save(update_fields=['puntos_obtenidos'])
                    actualizar_ranking_por_liga(
                        pronostico.fk_id_usuario,
                        pronostico.fk_id_liga,
                        diferencia,
                    )

        serializer = PartidoSerializer(partido)
        return Response(serializer.data)
    except Partido.DoesNotExist:
        return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)




# ------------------------------------------------------------------
# Bracket de eliminatorias
# ------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def bracket_eliminatoria(request):
    """
    Obtiene el bracket completo de eliminatorias para una liga.

    Query params:
        liga_id: ID de la liga

    Retorna estructura jerárquica con fases, partidos, equipos,
    resultados y conexiones entre partidos.
    """
    from .bracket_services import obtener_bracket

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

    ligas_usuario = obtener_ligas_usuario_ids(request.user.id_usuario)
    if liga_id_int not in ligas_usuario:
        raise PermissionDenied('No tienes permisos para consultar esta liga.')

    resultado = obtener_bracket(liga_id_int)
    if 'error' in resultado:
        return Response(resultado, status=status.HTTP_400_BAD_REQUEST)

    return Response(resultado)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def generar_bracket(request):
    """
    Genera automáticamente el bracket de eliminatorias para una liga.
    Solo administradores.

    Body params:
        liga_id: ID de la liga
        octavos: Lista de configuración de octavos de final
            [
                {
                    'slot': 'O1',
                    'equipo_local': id_seleccion,
                    'equipo_visitante': id_seleccion,
                    'horario': '2026-07-01T16:00:00Z',
                    'fk_sede': id_sede
                },
                ... (8 partidos)
            ]
    """
    from .bracket_services import generar_cruces_eliminatoria
    from django.utils.dateparse import parse_datetime

    liga_id = request.data.get('liga_id')
    octavos_data = request.data.get('octavos', [])

    if not liga_id:
        return Response(
            {'error': 'Se requiere el ID de la liga'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not octavos_data or len(octavos_data) != 8:
        return Response(
            {'error': 'Se requieren exactamente 8 partidos de octavos'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Normalizar fechas
    for item in octavos_data:
        if 'horario' in item and isinstance(item['horario'], str):
            item['horario'] = parse_datetime(item['horario'])

    resultado = generar_cruces_eliminatoria(int(liga_id), octavos_data)
    if 'error' in resultado:
        return Response(resultado, status=status.HTTP_400_BAD_REQUEST)

    return Response(resultado, status=status.HTTP_201_CREATED)
