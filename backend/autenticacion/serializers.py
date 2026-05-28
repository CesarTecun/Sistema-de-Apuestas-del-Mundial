import hashlib
import secrets
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from backend.usuarios.models import Usuario
from backend.autenticacion.models import PasswordResetToken
from .utils import generar_tokens_y_sesion, cerrar_todas_las_sesiones_usuario


def validar_contrasena(password, user=None):
    """Validador de contraseña con mensajes de error localizados."""
    try:
        validate_password(password, user)
    except DjangoValidationError as exc:
        mensajes_localizados = []
        for msg in exc.messages:
            if 'too common' in msg.lower():
                mensajes_localizados.append('Contraseña muy común. Elige una más segura.')
            elif 'too short' in msg.lower():
                import re
                match = re.search(r'(\d+)', msg)
                if match:
                    mensajes_localizados.append(
                        f'La contraseña es muy corta. Debe contener al menos {match.group(1)} caracteres.'
                    )
                else:
                    mensajes_localizados.append('La contraseña es muy corta.')
            elif 'too similar' in msg.lower():
                mensajes_localizados.append('La contraseña es muy similar a tus datos personales.')
            elif 'entirely numeric' in msg.lower():
                mensajes_localizados.append('La contraseña no puede ser completamente numérica.')
            else:
                mensajes_localizados.append(msg)
        raise DjangoValidationError(mensajes_localizados)


class UserSerializer(serializers.ModelSerializer):
    """Serializer para información del usuario"""
    class Meta:
        model = Usuario
        fields = (
            'id_usuario', 'email', 'primer_nombre', 'segundo_nombre',
            'primer_apellido', 'segundo_apellido', 'telefono',
            'fecha_nacimiento', 'fk_rol'
        )
        read_only_fields = ('id_usuario',)


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuarios"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validar_contrasena]
    )
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = (
            'email', 'primer_nombre', 'segundo_nombre',
            'primer_apellido', 'segundo_apellido', 'telefono',
            'fecha_nacimiento', 'password', 'password2', 'fk_rol'
        )
        extra_kwargs = {
            'fk_rol': {'required': False}
        }

    def validate(self, attrs):
        password2 = attrs.pop('password2', None)
        if password2 and attrs['password'] != password2:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Asignar rol por defecto (rol 2 = usuario normal)
        if 'fk_rol' not in validated_data:
            validated_data['fk_rol'] = 2
        # Incluir contrasena en validated_data antes de crear
        validated_data['contrasena'] = password
        user = Usuario.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para login de usuarios (usa email como username)"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Usar authenticate con email como username
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Usuario inactivo.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Credenciales inválidas.")
        else:
            raise serializers.ValidationError("Debe proporcionar email y password.")

        return data


class SessionTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer JWT que además registra la sesión en la BD."""

    def validate(self, attrs):
        data = super().validate(attrs)
        request = self.context.get('request')
        refresh, access, sesion = generar_tokens_y_sesion(self.user, request)

        data['refresh'] = refresh
        data['access'] = access
        data['user'] = UserSerializer(self.user).data
        data['sesion'] = {
            'id_sesion': sesion.id_sesion,
            'dispositivo': sesion.dispositivo,
            'ip_address': sesion.ip_address,
            'fecha_inicio': sesion.fecha_inicio,
        } if sesion else None
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return None, None

        token_plano = secrets.token_hex(32)
        token_hash = hashlib.sha256(token_plano.encode()).hexdigest()
        expires_at = timezone.now() + timedelta(hours=24)
        token_obj = PasswordResetToken.objects.create(
            usuario=usuario,
            token_hash=token_hash,
            expires_at=expires_at
        )
        return token_obj, token_plano


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, validators=[validar_contrasena])
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden.'})

        token_hash = hashlib.sha256(attrs['token'].encode()).hexdigest()
        try:
            token_obj = PasswordResetToken.objects.get(token_hash=token_hash)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({'token': 'Token inválido o expirado.'})

        if not token_obj.is_active:
            raise serializers.ValidationError({'token': 'Token inválido o expirado.'})

        self.context['token_obj'] = token_obj
        return attrs

    def save(self, **kwargs):
        token_obj = self.context['token_obj']
        usuario = token_obj.usuario
        password = self.validated_data['password']

        usuario.set_password(password)
        usuario.save(update_fields=['contrasena'])
        token_obj.mark_used()

        # Invalidar todas las sesiones activas del usuario tras cambiar contraseña
        cerrar_todas_las_sesiones_usuario(usuario.id_usuario)

        return usuario


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambio de contraseña desde el perfil autenticado."""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validar_contrasena])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': 'Las contraseñas no coinciden.'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['contrasena'])
        # Invalidar todas las sesiones activas del usuario
        cerrar_todas_las_sesiones_usuario(user.id_usuario)
        return user



