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
            try:
                liga_id = int(liga_id)
                queryset = queryset.filter(fk_id_liga=liga_id)
            except ValueError:
                return queryset.none()
        if partido_id:
            try:
                partido_id = int(partido_id)
                queryset = queryset.filter(fk_id_partido=partido_id)
            except ValueError:
                return queryset.none()

        return queryset

    def perform_create(self, serializer):
        usuario_id = self.request.user.id_usuario
        liga_id = serializer.validated_data.get('fk_id_liga')
        partido_id = serializer.validated_data.get('fk_id_partido')

        if not liga_id or liga_id not in obtener_ligas_usuario_ids(usuario_id):
            raise PermissionDenied('No tienes permisos para pronosticar en esta liga.')

        if not Partido.objects.filter(id_partido=partido_id, fk_id_liga=liga_id).exists():
            raise ValidationError({'fk_id_partido': 'El partido no pertenece a la liga seleccionada.'})

        # Buscar pronóstico existente incluyendo eliminados lógicamente
        pronostico_existente = Pronostico.all_objects.filter(
            fk_id_usuario=usuario_id,
            fk_id_partido=partido_id,
            fk_id_liga=liga_id
        ).first()

        if pronostico_existente:
            if pronostico_existente.status:
                raise ValidationError({'detail': 'Ya registraste un pronóstico para este partido en esta liga.'})
            # Reactivar el pronóstico eliminado con los nuevos valores
            pronostico_existente.gol_local = serializer.validated_data.get('gol_local')
            pronostico_existente.gol_visitante = serializer.validated_data.get('gol_visitante')
            pronostico_existente.puntos_obtenidos = 0
            pronostico_existente.status = True
            pronostico_existente.deleted_at = None
            pronostico_existente.save()
            serializer.instance = pronostico_existente
            return

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
    
    try:
        usuario_id_int = int(usuario_id)
    except ValueError:
        return Response({'error': 'usuario_id debe ser numérico'}, status=status.HTTP_400_BAD_REQUEST)
    
    pronosticos = Pronostico.objects.filter(fk_id_usuario=usuario_id_int)
    serializer = PronosticoSerializer(pronosticos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pronosticos_por_liga(request):
    """Obtener pronósticos de una liga específica"""
    liga_id = request.query_params.get('liga_id')
    if not liga_id:
        return Response({'error': 'Se requiere el ID de la liga'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        liga_id_int = int(liga_id)
    except ValueError:
        return Response({'error': 'liga_id debe ser numérico'}, status=status.HTTP_400_BAD_REQUEST)
    
    pronosticos = Pronostico.objects.filter(fk_id_liga=liga_id_int)
    serializer = PronosticoSerializer(pronosticos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pronosticos_por_partido(request):
    """Obtener pronósticos de un partido específico"""
    partido_id = request.query_params.get('partido_id')
    if not partido_id:
        return Response({'error': 'Se requiere el ID del partido'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        partido_id_int = int(partido_id)
    except ValueError:
        return Response({'error': 'partido_id debe ser numérico'}, status=status.HTTP_400_BAD_REQUEST)

    pronosticos = Pronostico.objects.filter(fk_id_partido=partido_id_int)
    serializer = PronosticoSerializer(pronosticos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pronosticos_por_partido_liga(request):
    """Obtener pronósticos de un partido específico filtrados por liga"""
    partido_id = request.query_params.get('partido_id')
    liga_id = request.query_params.get('liga_id')
    
    if not partido_id or not liga_id:
        return Response(
            {'error': 'Se requieren los IDs del partido y la liga'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        partido_id_int = int(partido_id)
        liga_id_int = int(liga_id)
    except ValueError:
        return Response(
            {'error': 'Los IDs deben ser numéricos'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    pronosticos = Pronostico.objects.filter(
        fk_id_partido=partido_id_int,
        fk_id_liga=liga_id_int
    )
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
    
    try:
        usuario_id_int = int(usuario_id)
        liga_id_int = int(liga_id)
    except ValueError:
        return Response(
            {'error': 'Los IDs deben ser numéricos'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    pronosticos = Pronostico.objects.filter(
        fk_id_usuario=usuario_id_int,
        fk_id_liga=liga_id_int
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
    
    try:
        usuario_id_int = int(usuario_id)
        partido_id_int = int(partido_id)
        liga_id_int = int(liga_id)
    except ValueError:
        return Response(
            {'error': 'Los IDs deben ser numéricos'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    existe = Pronostico.objects.filter(
        fk_id_usuario=usuario_id_int,
        fk_id_partido=partido_id_int,
        fk_id_liga=liga_id_int
    ).exists()
    
    return Response({
        'disponible': not existe,
        'mensaje': 'Pronóstico disponible' if not existe else 'Ya existe un pronóstico para este partido'
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def historial_usuario(request):
    """
    Historial completo del usuario autenticado:
    - Pronósticos con detalle de partidos, puntos y aciertos
    - Resumen por liga (puntos, posición, partidos jugados, aciertos)
    """
    from django.db import models
    from backend.pronosticos.models import Pronostico
    from backend.partidos.models import Partido, Seleccion
    from backend.posiciones.models import Ranking
    from backend.ligas.models import Liga

    try:
        usuario_id = request.user.id_usuario
        pronosticos = Pronostico.objects.filter(fk_id_usuario=usuario_id, status=True)

        detalle_pronosticos = []
        partido_ids = {p.fk_id_partido for p in pronosticos}
        partidos = {p.id_partido: p for p in Partido.objects.filter(id_partido__in=partido_ids)}
        selecciones = {s.id_seleccion: s for s in Seleccion.objects.all()}

        for pronostico in pronosticos:
            partido = partidos.get(pronostico.fk_id_partido)
            if not partido:
                continue

            # Datos del partido
            local = selecciones.get(partido.equipo_local)
            visitante = selecciones.get(partido.equipo_visitante)
            resultado_real = f"{partido.gol_local} - {partido.gol_visitante}" if partido.gol_local is not None else "Pendiente"
            resultado_pronosticado = f"{pronostico.gol_local} - {pronostico.gol_visitante}"

            # Determinar tipo de acierto
            puntos = pronostico.puntos_obtenidos
            if puntos == 3:
                tipo_acierto = "Marcador exacto"
            elif puntos == 1:
                tipo_acierto = "Resultado correcto"
            elif partido.estado_partido == 'finalizado':
                tipo_acierto = "Fallido"
            else:
                tipo_acierto = "Pendiente"

            detalle_pronosticos.append({
                "id_pronostico": pronostico.id_pronostico,
                "fk_id_partido": pronostico.fk_id_partido,
                "fk_id_liga": pronostico.fk_id_liga,
                "equipo_local": local.pais if local else "Desconocido",
                "equipo_visitante": visitante.pais if visitante else "Desconocido",
                "gol_local_pronostico": pronostico.gol_local,
                "gol_visitante_pronostico": pronostico.gol_visitante,
                "gol_local_real": partido.gol_local,
                "gol_visitante_real": partido.gol_visitante,
                "resultado_real": resultado_real,
                "resultado_pronosticado": resultado_pronosticado,
                "puntos_obtenidos": puntos,
                "tipo_acierto": tipo_acierto,
                "estado_partido": partido.estado_partido,
                "horario": partido.horario.isoformat() if partido.horario else None,
            })

        # Ordenar: más recientes primero
        detalle_pronosticos.sort(key=lambda x: x["horario"] or "", reverse=True)

        # Resumen por liga
        ligas_ids = {p.fk_id_liga for p in pronosticos}
        ligas = {l.id_liga: l for l in Liga.objects.filter(id_liga__in=ligas_ids)}
        from backend.ligas.models import ParticipanteLiga

        resumen_ligas = []
        for liga_id in ligas_ids:
            pronosticos_liga = [p for p in pronosticos if p.fk_id_liga == liga_id]
            liga = ligas.get(liga_id)

            partidos_jugados = len(pronosticos_liga)
            puntos_totales = sum(p.puntos_obtenidos for p in pronosticos_liga)
            marcadores_exactos = sum(1 for p in pronosticos_liga if p.puntos_obtenidos == 3)
            resultados_correctos = sum(1 for p in pronosticos_liga if p.puntos_obtenidos == 1)
            fallidos = sum(1 for p in pronosticos_liga if p.puntos_obtenidos == 0 and p.fk_id_partido in partidos and partidos[p.fk_id_partido].estado_partido == 'finalizado')

            # Calcular posición basada en puntos (solo usuarios que han participado)
            from backend.pronosticos.models import Pronostico
            from django.db.models import Sum, OuterRef, Subquery

            # Obtener usuarios que han hecho al menos un pronóstico en esta liga
            usuarios_con_pronosticos = Pronostico.objects.filter(
                fk_id_liga=liga_id
            ).values_list('fk_id_usuario', flat=True).distinct()

            # Obtener puntos de cada usuario
            puntos_subquery = Pronostico.objects.filter(
                fk_id_usuario=OuterRef('fk_id_usuario'),
                fk_id_liga=OuterRef('fk_id_liga')
            ).values('fk_id_usuario').annotate(
                total=Sum('puntos_obtenidos')
            ).values('total')[:1]

            # Obtener participantes ordenados por puntos descendentes
            todos_participantes = ParticipanteLiga.objects.filter(
                fk_id_liga=liga_id,
                fk_id_usuario__in=usuarios_con_pronosticos
            ).annotate(
                puntos_totales=Subquery(puntos_subquery, output_field=models.IntegerField())
            ).order_by('-puntos_totales', 'fecha_union')

            # Calcular la posición del usuario (1-based index)
            posicion = None
            for idx, participante in enumerate(todos_participantes, start=1):
                if participante.fk_id_usuario == usuario_id:
                    posicion = idx
                    break

            if posicion == 1:
                estado_liga = "Ganada"
            elif posicion:
                estado_liga = f"Posición {posicion}"
            else:
                estado_liga = "Sin posición"

            resumen_ligas.append({
                "liga_id": liga_id,
                "liga_nombre": liga.nombre_liga if liga else f"Liga {liga_id}",
                "puntos_totales": puntos_totales,
                "partidos_jugados": partidos_jugados,
                "marcadores_exactos": marcadores_exactos,
                "resultados_correctos": resultados_correctos,
                "fallidos": fallidos,
                "posicion": posicion,
                "estado_liga": estado_liga,
            })

        # Ordenar ligas por puntos descendente
        resumen_ligas.sort(key=lambda x: x["puntos_totales"], reverse=True)

        return Response({
            "usuario_id": usuario_id,
            "total_pronosticos": len(pronosticos),
            "puntos_totales": sum(p.puntos_obtenidos for p in pronosticos),
            "pronosticos": detalle_pronosticos,
            "resumen_ligas": resumen_ligas,
        })
    except Exception as exc:
        import traceback
        traceback.print_exc()
        return Response(
            {"error": str(exc), "detail": "Error interno al generar el historial"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
