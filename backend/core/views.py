from django.db.models import Sum
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Sede, FaseGrupo, Bitacora, AuditLog, ConfiguracionTorneo
from .serializers import (
    SedeSerializer, FaseGrupoSerializer,
    BitacoraSerializer, AuditLogSerializer, ConfiguracionTorneoSerializer,
)


class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id_sede'


class FaseGrupoViewSet(viewsets.ModelViewSet):
    queryset = FaseGrupo.objects.all()
    serializer_class = FaseGrupoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id_fase'


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def sedes_lista(request):
    sedes = Sede.objects.all()
    serializer = SedeSerializer(sedes, many=True)
    return Response(serializer.data)


# ──────────────────────────────────────────────
# M7 — Bitácora y Auditoría
# ──────────────────────────────────────────────

class BitacoraViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista entradas de bitácora. Solo administradores."""
    serializer_class = BitacoraSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = Bitacora.objects.all()
        usuario_id = self.request.query_params.get('usuario_id')
        fecha = self.request.query_params.get('fecha')
        if usuario_id:
            qs = qs.filter(fk_id_usuario=usuario_id)
        if fecha:
            qs = qs.filter(fecha=fecha)
        return qs.order_by('-fecha', '-hora')


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista entradas del log de auditoría. Solo administradores."""
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = AuditLog.objects.all()
        tabla = self.request.query_params.get('table_name')
        operacion = self.request.query_params.get('operation')
        if tabla:
            qs = qs.filter(table_name=tabla)
        if operacion:
            qs = qs.filter(operation=operacion)
        return qs.order_by('-changed_at')


# ──────────────────────────────────────────────
# M7 — Configuración del torneo
# ──────────────────────────────────────────────

class ConfiguracionTorneoView(APIView):
    """GET/PUT de la configuración global del torneo. Solo administradores."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        config = ConfiguracionTorneo.get_config()
        return Response(ConfiguracionTorneoSerializer(config).data)

    def put(self, request):
        config = ConfiguracionTorneo.get_config()
        serializer = ConfiguracionTorneoSerializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ──────────────────────────────────────────────
# M7 — Reporte / Dashboard
# ──────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def reporte_resumen(request):
    """Resumen global del sistema para el dashboard administrativo."""
    from backend.usuarios.models import Usuario
    from backend.ligas.models import Liga, ParticipanteLiga
    from backend.partidos.models import Partido
    from backend.pronosticos.models import Pronostico
    from backend.autenticacion.models import SesionUsuario
    from backend.premios.models import Premio

    return Response({
        'usuarios': {
            'total': Usuario.all_objects.count(),
            'activos': Usuario.objects.count(),
            'inactivos': Usuario.all_objects.filter(status=False).count(),
            'admins': Usuario.all_objects.filter(fk_rol=1).count(),
        },
        'sesiones': {
            'activas_ahora': SesionUsuario.objects.filter(estado_sesion='Activa').count(),
        },
        'ligas': {
            'total': Liga.all_objects.count(),
            'activas': Liga.objects.count(),
            'publicas': Liga.objects.filter(es_publica=True).count(),
            'competitivas': Liga.objects.filter(tipo_liga='Competitiva').count(),
        },
        'partidos': {
            'total': Partido.all_objects.count(),
            'programados': Partido.objects.filter(estado_partido='programado').count(),
            'en_juego': Partido.objects.filter(estado_partido='en_juego').count(),
            'finalizados': Partido.objects.filter(estado_partido='finalizado').count(),
        },
        'pronosticos': {
            'total': Pronostico.all_objects.count(),
        },
        'premios': {
            'total_recaudado': float(
                Liga.all_objects.aggregate(total=Sum('monto_total_recaudado'))['total'] or 0
            ),
            'total_distribuido': float(
                Premio.objects.aggregate(total=Sum('monto_premio'))['total'] or 0
            ),
        },
        'generado_en': timezone.now(),
    })
