from rest_framework import serializers
from .models import Partido, Jugador, Seleccion


class PartidoSerializer(serializers.ModelSerializer):
    resultado_display = serializers.ReadOnlyField()
    ganador = serializers.ReadOnlyField()

    class Meta:
        model = Partido
        fields = '__all__'
        read_only_fields = ('id_partido',)

    def validate(self, data):
        """Validación personalizada para los goles"""
        if data.get('gol_local', 0) < 0:
            raise serializers.ValidationError("Los goles del equipo local no pueden ser negativos")
        if data.get('gol_visitante', 0) < 0:
            raise serializers.ValidationError("Los goles del equipo visitante no pueden ser negativos")
        return data


class JugadorSerializer(serializers.ModelSerializer):
    """Serializer para gestionar jugadores con soft delete"""

    class Meta:
        model = Jugador
        fields = [
            'id_jugador',
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'fecha_nacimiento',
            'dorsal',
            'posicion',
            'fk_id_seleccion',
            'status'
        ]
        read_only_fields = ('id_jugador',)


class SeleccionSerializer(serializers.ModelSerializer):
    """Serializer para gestionar selecciones con soft delete"""

    class Meta:
        model = Seleccion
        fields = [
            'id_seleccion',
            'pais',
            'bandera',
            'fk_id_fase_inicial',
            'status'
        ]
        read_only_fields = ('id_seleccion',)
