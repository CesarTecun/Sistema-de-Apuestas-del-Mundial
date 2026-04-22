from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from backend.usuarios.models import Usuario


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
        validators=[validate_password]
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
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("Usuario inactivo.")
            else:
                raise serializers.ValidationError("Credenciales inválidas.")
        else:
            raise serializers.ValidationError("Debe proporcionar email y password.")

        return data
