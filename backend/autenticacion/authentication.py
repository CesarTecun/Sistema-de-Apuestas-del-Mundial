"""Autenticadores personalizados para el módulo de autenticación."""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import SesionUsuario


class SesionJWTAuthentication(JWTAuthentication):
    """Valida que el JWT pertenezca a una sesión activa registrada en BD."""

    def authenticate(self, request):
        authenticated = super().authenticate(request)
        if authenticated is None:
            return None

        user, validated_token = authenticated
        sesion_id = validated_token.get("sesion_id")

        if sesion_id is None:
            raise AuthenticationFailed(
                "El token no tiene una sesión asociada. Inicia sesión nuevamente."
            )

        try:
            sesion = SesionUsuario.objects.get(
                id_sesion=sesion_id,
                fk_id_usuario=user.id_usuario,
            )
        except SesionUsuario.DoesNotExist as exc:
            raise AuthenticationFailed(
                "Sesión inválida. Inicia sesión nuevamente."
            ) from exc

        if sesion.estado_sesion != "Activa":
            raise AuthenticationFailed("La sesión fue cerrada. Inicia sesión nuevamente.")

        request.sesion_usuario = sesion
        return user, validated_token
