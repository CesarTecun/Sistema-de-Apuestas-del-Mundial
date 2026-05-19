from rest_framework import serializers
from .models import Sede, FaseGrupo


class SedeSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Sede"""
    class Meta:
        model = Sede
        fields = ['id_sede', 'ciudad', 'estadio']
        read_only_fields = ['id_sede']


class FaseGrupoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo FaseGrupo"""
    class Meta:
        model = FaseGrupo
        fields = ['id_fase', 'nombre_fase']
        read_only_fields = ['id_fase']
