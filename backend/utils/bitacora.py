from backend.core.models import Bitacora


def registrar_bitacora(usuario_id, accion):
    """Crea una entrada en la bitácora de forma segura (no lanza excepciones)."""
    try:
        Bitacora.objects.create(
            fk_id_usuario=usuario_id,
            detalle_accion=accion,
        )
    except Exception:
        pass
