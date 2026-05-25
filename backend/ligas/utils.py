from typing import Set

from backend.ligas.models import Liga, ParticipanteLiga, Invitacion


def obtener_ligas_usuario_ids(usuario_id: int) -> Set[int]:
    """IDs de las ligas donde el usuario es admin, participante activo, tiene invitación válida, o son públicas."""
    ligas_admin = Liga.objects.filter(fk_administrador=usuario_id).values_list('id_liga', flat=True)

    ligas_participante = ParticipanteLiga.objects.filter(
        fk_id_usuario=usuario_id,
        estado_participacion='Activo'
    ).values_list('fk_id_liga', flat=True)

    ligas_invitacion = Invitacion.objects.filter(
        fk_id_usuario_invitado=usuario_id,
        estado_invitacion__in=['Pendiente', 'Aceptada']
    ).values_list('fk_id_liga', flat=True)

    ligas_publicas = Liga.objects.filter(
        es_publica=True,
        status=True
    ).values_list('id_liga', flat=True)

    return set(ligas_admin) | set(ligas_participante) | set(ligas_invitacion) | set(ligas_publicas)


def obtener_ligas_administradas_ids(usuario_id: int) -> Set[int]:
    """IDs de las ligas donde el usuario es administrador (dueño).
    También incluye ligas públicas sin administrador, para que cualquier
    usuario autenticado pueda gestionar sus partidos."""
    admin_ids = set(
        Liga.objects.filter(fk_administrador=usuario_id).values_list('id_liga', flat=True)
    )
    publicas_sin_admin = set(
        Liga.objects.filter(
            es_publica=True,
            fk_administrador__isnull=True,
            status=True
        ).values_list('id_liga', flat=True)
    )
    return admin_ids | publicas_sin_admin
