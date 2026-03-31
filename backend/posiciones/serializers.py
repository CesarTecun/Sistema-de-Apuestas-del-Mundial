from rest_framework import serializers
from .models import Ranking


class RankingSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Ranking"""
    
    class Meta:
        model = Ranking
        fields = ['id_registro', 'puntos', 'fk_id_usuario', 'fk_id_liga', 'pj', 'fecha_actualizacion']
        read_only_fields = ('id_registro', 'fecha_actualizacion')


class RankingConPosicionSerializer(serializers.Serializer):
    """Serializador para mostrar ranking con posición calculada"""
    posicion = serializers.IntegerField()
    usuario_id = serializers.IntegerField()
    puntos = serializers.IntegerField()
    pj = serializers.IntegerField()
    fecha_actualizacion = serializers.DateTimeField()


class PosicionUsuarioSerializer(serializers.Serializer):
    """Serializador para mostrar la posición detallada de un usuario"""
    usuario_id = serializers.IntegerField()
    liga_id = serializers.IntegerField()
    puntos = serializers.IntegerField()
    pj = serializers.IntegerField()
    aciertos_exactos = serializers.IntegerField()
    aciertos_ganador = serializers.IntegerField()
