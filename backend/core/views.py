from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Sede, FaseGrupo
from .serializers import SedeSerializer, FaseGrupoSerializer


class SedeViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar sedes
    """
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id_sede'


class FaseGrupoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar fases de grupos
    """
    queryset = FaseGrupo.objects.all()
    serializer_class = FaseGrupoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id_fase'


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def sedes_lista(request):
    """Obtener lista de todas las sedes"""
    sedes = Sede.objects.all()
    serializer = SedeSerializer(sedes, many=True)
    return Response(serializer.data)
