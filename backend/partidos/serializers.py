from rest_framework import serializers
from .models import Partido

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
