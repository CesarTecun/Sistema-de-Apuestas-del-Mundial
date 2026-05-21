"""
Utilidades para el manejo de sesiones de usuario.
"""
import hashlib
import uuid
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .models import SesionUsuario


def crear_sesion_usuario(usuario, request, refresh_token: str | None = None, jwt_jti: str | None = None):
    """
    Crea un nuevo registro de sesión para un usuario.

    Args:
        usuario: Instancia del modelo Usuario
        request: HttpRequest con información del cliente

    Returns:
        SesionUsuario: La sesión creada o None si falla
    """
    try:
        # Obtener información del request
        ip_address = _get_ip_address(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        dispositivo = _detectar_dispositivo(user_agent)

        # Generar token de sesión único
        token_sesion = _build_token_value(refresh_token)

        # Crear sesión en la base de datos
        sesion = SesionUsuario.objects.create(
            fk_id_usuario=usuario.id_usuario,
            token_sesion=token_sesion,
            refresh_token_hash=_hash_token(refresh_token) if refresh_token else None,
            jwt_jti=jwt_jti,
            estado_sesion='Activa',
            ip_address=ip_address,
            user_agent=user_agent,
            dispositivo=dispositivo
        )

        # Guardar token en session de Django
        request.session['token_sesion'] = token_sesion
        request.session['id_sesion'] = sesion.id_sesion

        return sesion

    except Exception as e:
        print(f"Error creando sesión: {e}")
        return None


def cerrar_sesion_usuario(request, refresh_token: str | None = None):
    """
    Cierra la sesión activa del usuario.

    Args:
        request: HttpRequest con la sesión a cerrar

    Returns:
        bool: True si se cerró correctamente, False en caso contrario
    """
    try:
        token_sesion = request.session.get('token_sesion') or _hash_token(refresh_token)

        if token_sesion:
            # Buscar y cerrar sesión por token
            sesion = SesionUsuario.objects.filter(
                token_sesion=token_sesion,
                estado_sesion='Activa'
            ).first()

            if sesion:
                sesion.estado_sesion = 'Cerrada'
                sesion.fecha_cierre = timezone.now()
                sesion.save(update_fields=['estado_sesion', 'fecha_cierre'])

        # También intentar cerrar por usuario si no hay token
        if hasattr(request, 'user') and request.user.is_authenticated:
            SesionUsuario.objects.filter(
                fk_id_usuario=request.user.id_usuario,
                estado_sesion='Activa'
            ).update(
                estado_sesion='Cerrada',
                fecha_cierre=timezone.now()
            )

        # Limpiar session de Django
        if 'token_sesion' in request.session:
            del request.session['token_sesion']
        if 'id_sesion' in request.session:
            del request.session['id_sesion']

        return True

    except Exception as e:
        print(f"Error cerrando sesión: {e}")
        return False


def actualizar_actividad_sesion(request):
    """
    Actualiza la última actividad de la sesión activa.

    Args:
        request: HttpRequest

    Returns:
        bool: True si se actualizó, False en caso contrario
    """
    try:
        token_sesion = request.session.get('token_sesion')

        if token_sesion:
            SesionUsuario.objects.filter(
                token_sesion=token_sesion,
                estado_sesion='Activa'
            ).update(
                fecha_ultima_actividad=timezone.now()
            )
            return True

        # Fallback: buscar por usuario
        if hasattr(request, 'user') and request.user.is_authenticated:
            sesion = SesionUsuario.objects.filter(
                fk_id_usuario=request.user.id_usuario,
                estado_sesion='Activa'
            ).order_by('-fecha_ultima_actividad').first()

            if sesion:
                sesion.fecha_ultima_actividad = timezone.now()
                sesion.save(update_fields=['fecha_ultima_actividad'])
                return True

        return False

    except Exception as e:
        print(f"Error actualizando actividad: {e}")
        return False


def obtener_sesiones_activas(usuario_id):
    """
    Obtiene todas las sesiones activas de un usuario.

    Args:
        usuario_id: ID del usuario

    Returns:
        QuerySet: Sesiones activas del usuario
    """
    return SesionUsuario.objects.filter(
        fk_id_usuario=usuario_id,
        estado_sesion='Activa'
    ).order_by('-fecha_ultima_actividad')


def _get_ip_address(request):
    """Obtiene la IP del request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip[:45] if ip else None


def _detectar_dispositivo(user_agent):
    """Detecta el tipo de dispositivo."""
    user_agent_lower = user_agent.lower()

    if 'mobile' in user_agent_lower or 'android' in user_agent_lower or 'iphone' in user_agent_lower:
        return 'Móvil'
    elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
        return 'Tablet'
    elif 'windows' in user_agent_lower or 'macintosh' in user_agent_lower or 'linux' in user_agent_lower:
        return 'Escritorio'
    else:
        return 'Desconocido'


def _hash_token(token: str | None) -> str | None:
    if not token:
        return None
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def _build_token_value(refresh_token: str | None) -> str:
    """Usa el hash del refresh token como identificador o genera uuid."""
    return _hash_token(refresh_token) or str(uuid.uuid4())


def generar_tokens_y_sesion(usuario, request):
    """Genera tokens JWT y registra la sesión asociada."""
    refresh_obj = RefreshToken.for_user(usuario)
    refresh = str(refresh_obj)
    access = str(refresh_obj.access_token)
    sesion = crear_sesion_usuario(
        usuario,
        request,
        refresh_token=refresh,
        jwt_jti=str(refresh_obj.get('jti'))
    )
    return refresh, access, sesion
