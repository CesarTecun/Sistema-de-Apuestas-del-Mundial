"""
Vistas proxy para exponer los endpoints del microservicio Marcador
a través del backend Django. El frontend consume estos endpoints
como si fueran nativos del proyecto.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from backend.marcador_client import MarcadorClient, MarcadorClientError


client = MarcadorClient()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def marcador_selecciones(request):
    """Proxy: listar selecciones del microservicio marcador."""
    try:
        data = client.listar_selecciones()
        return Response(data)
    except MarcadorClientError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def marcador_partidos(request):
    """Proxy: listar partidos del microservicio marcador."""
    estado = request.query_params.get("estado")
    fk_id_liga = request.query_params.get("fk_id_liga")
    try:
        if fk_id_liga is not None:
            fk_id_liga = int(fk_id_liga)
        data = client.listar_partidos(estado=estado, fk_id_liga=fk_id_liga)
        return Response(data)
    except ValueError:
        return Response({"error": "fk_id_liga debe ser numérico"}, status=status.HTTP_400_BAD_REQUEST)
    except MarcadorClientError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def marcador_partidos_en_vivo(request):
    """Proxy: obtener partidos en juego desde el microservicio marcador."""
    try:
        data = client.partidos_en_vivo()
        return Response(data)
    except MarcadorClientError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def marcador_partido_detalle(request, id_partido):
    """Proxy: obtener detalle de un partido del microservicio marcador."""
    try:
        data = client.obtener_partido(id_partido)
        return Response(data)
    except MarcadorClientError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def marcador_partidos_por_equipo(request):
    """Proxy: obtener partidos por equipo desde el microservicio marcador."""
    equipo_id = request.query_params.get("equipo_id")
    if not equipo_id:
        return Response({"error": "Se requiere equipo_id"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        equipo_id = int(equipo_id)
        data = client.partidos_por_equipo(equipo_id)
        return Response(data)
    except ValueError:
        return Response({"error": "equipo_id debe ser numérico"}, status=status.HTTP_400_BAD_REQUEST)
    except MarcadorClientError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def marcador_crear_partido(request):
    """Proxy: crear partido en el microservicio marcador."""
    try:
        data = client.crear_partido(request.data)
        return Response(data, status=status.HTTP_201_CREATED)
    except MarcadorClientError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def marcador_actualizar_partido(request, id_partido):
    """Proxy: actualizar partido en el microservicio marcador."""
    try:
        data = client.actualizar_partido(id_partido, request.data)
        return Response(data)
    except MarcadorClientError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def marcador_actualizar_marcador(request, id_partido):
    """
    Proxy: actualizar marcador de un partido en el microservicio.
    Equivalente a actualizar-resultado pero apunta al microservicio.
    """
    try:
        data = client.actualizar_marcador(id_partido, request.data)
        return Response(data)
    except MarcadorClientError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def marcador_eliminar_partido(request, id_partido):
    """Proxy: eliminar partido del microservicio marcador."""
    try:
        client.eliminar_partido(id_partido)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except MarcadorClientError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def marcador_health(request):
    """Verificar estado de conexión con el microservicio marcador."""
    try:
        data = client.health_check()
        return Response({"marcador_service": data, "connected": data.get("status") == "ok"})
    except MarcadorClientError as exc:
        return Response(
            {"marcador_service": {"status": "unavailable"}, "connected": False, "error": str(exc)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@api_view(["POST"])
def marcador_webhook(request):
    """
    Webhook que recibe notificaciones del microservicio marcador
    cuando cambia un marcador. Actualiza el partido en Django.
    Usa un flag para evitar bucles de sincronización.
    """
    from .models import Partido
    from .signals import set_sync_from_webhook

    id_partido = request.data.get("id_partido")
    if not id_partido:
        return Response({"error": "id_partido requerido"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        partido = Partido.objects.get(id_partido=id_partido)
    except Partido.DoesNotExist:
        return Response({"error": "Partido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Desactivar la señal de sincronización para evitar bucles
    set_sync_from_webhook(True)
    try:
        # Actualizar campos del marcador si vienen en el payload
        update_fields = []
        if "gol_local" in request.data:
            partido.gol_local = request.data["gol_local"]
            update_fields.append("gol_local")
        if "gol_visitante" in request.data:
            partido.gol_visitante = request.data["gol_visitante"]
            update_fields.append("gol_visitante")
        if "estado" in request.data:
            partido.estado = request.data["estado"]
            update_fields.append("estado")
        if "resultado" in request.data:
            partido.resultado = request.data["resultado"]
            update_fields.append("resultado")
        if "ganador_penales" in request.data:
            partido.ganador_penales = request.data["ganador_penales"]
            update_fields.append("ganador_penales")

        if update_fields:
            partido.save(update_fields=update_fields)
    finally:
        set_sync_from_webhook(False)

    return Response({"message": "Partido actualizado desde marcador", "id_partido": partido.id_partido})
