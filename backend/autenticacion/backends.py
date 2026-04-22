from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from backend.usuarios.models import Usuario


class EmailAuthBackend(BaseBackend):
    """
    Backend de autenticación personalizado que permite
    autenticar usando email en lugar de username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # El campo 'username' puede contener el email
        email = username or kwargs.get('email')

        if not email or not password:
            return None

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return None

        # Verificar la contraseña contra el campo 'contrasena'
        # que está almacenado en formato Django (pbkdf2_sha256)
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
