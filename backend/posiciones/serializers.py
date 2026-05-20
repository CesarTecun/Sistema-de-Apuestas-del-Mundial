from rest_framework import serializers
from .models import Ranking, HistorialRanking
from backend.core.models import PosicionesTorneo


class RankingSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Ranking"""

    class Meta:
        model = Ranking
        fields = ['id_registro', 'puntos', 'fk_id_usuario', 'fk_id_liga', 'pj',
                  'posicion', 'posicion_anterior', 'fecha_actualizacion']
        read_only_fields = ('id_registro', 'fecha_actualizacion')


class RankingConPosicionSerializer(serializers.Serializer):
    """Serializador para mostrar ranking con posición calculada y variación"""
    posicion = serializers.IntegerField()
    posicion_anterior = serializers.IntegerField(allow_null=True)
    variacion = serializers.IntegerField()  # posicion_anterior - posicion
    tendencia = serializers.CharField()     # 'subio', 'bajo', 'igual'
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


class HistorialRankingSerializer(serializers.ModelSerializer):
    """Serializador para el modelo HistorialRanking"""

    class Meta:
        model = HistorialRanking
        fields = ['id_historial', 'fk_id_usuario', 'fk_id_liga', 'puntos', 'pj',
                  'posicion', 'jornada', 'fecha_registro']


class TablaPosicionEquipoSerializer(serializers.ModelSerializer):
    """Serializador para la tabla de posiciones FIFA por liga"""
    nombre_seleccion = serializers.SerializerMethodField()
    bandera_seleccion = serializers.SerializerMethodField()
    variacion = serializers.SerializerMethodField()
    tendencia = serializers.SerializerMethodField()

    class Meta:
        model = PosicionesTorneo
        fields = [
            'id_posicion', 'fk_id_seleccion', 'nombre_seleccion', 'bandera_seleccion',
            'fk_id_liga', 'pj', 'pg', 'pe', 'pp', 'gf', 'gc', 'dg', 'puntos',
            'posicion', 'posicion_anterior', 'variacion', 'tendencia', 'fecha_actualizacion'
        ]

    def get_nombre_seleccion(self, obj):
        from backend.partidos.models import Seleccion
        try:
            return Seleccion.objects.get(id_seleccion=obj.fk_id_seleccion).pais
        except Seleccion.DoesNotExist:
            return None

    def get_bandera_seleccion(self, obj):
        from backend.partidos.models import Seleccion
        try:
            return Seleccion.objects.get(id_seleccion=obj.fk_id_seleccion).bandera
        except Seleccion.DoesNotExist:
            return None

    def get_variacion(self, obj):
        if obj.posicion_anterior is None or obj.posicion is None:
            return 0
        return obj.posicion_anterior - obj.posicion

    def get_tendencia(self, obj):
        if obj.posicion_anterior is None or obj.posicion is None:
            return 'igual'
        if obj.posicion < obj.posicion_anterior:
            return 'subio'
        if obj.posicion > obj.posicion_anterior:
            return 'bajo'
        return 'igual'
