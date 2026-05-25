from rest_framework import serializers
from .models import Usuario, RolUsuario


class RolUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolUsuario
        fields = ['id_rol', 'descripcion']


class AdminUsuarioSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'id_usuario', 'email', 'primer_nombre', 'segundo_nombre',
            'primer_apellido', 'segundo_apellido', 'telefono',
            'fecha_nacimiento', 'fk_rol', 'status', 'deleted_at',
            'nombre_completo',
        ]
        read_only_fields = ['id_usuario', 'email', 'deleted_at', 'nombre_completo']

    def get_nombre_completo(self, obj):
        return obj.get_full_name()
