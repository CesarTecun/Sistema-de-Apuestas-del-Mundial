from rest_framework import serializers
from .models import Premio


class PremioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Premio"""
    
    class Meta:
        model = Premio
        fields = ['id_premio', 'fk_id_liga', 'posicion', 'porcentaje_premio']
        read_only_fields = ('id_premio',)


class PremioCalculadoSerializer(serializers.Serializer):
    """Serializador para mostrar premios calculados con montos"""
    posicion = serializers.IntegerField()
    usuario_id = serializers.IntegerField()
    puntos = serializers.IntegerField()
    porcentaje = serializers.FloatField()
    monto_premio = serializers.FloatField()


class DistribucionPremiosSerializer(serializers.Serializer):
    """Serializador para mostrar la distribución completa de premios de una liga"""
    liga_id = serializers.IntegerField()
    nombre_liga = serializers.CharField()
    monto_total_recaudado = serializers.FloatField()
    total_participantes = serializers.IntegerField()
    premios = PremioCalculadoSerializer(many=True)
    total_distribuido = serializers.FloatField()
    remanente = serializers.FloatField()


class PremioUsuarioSerializer(serializers.Serializer):
    """Serializador para mostrar el premio de un usuario específico"""
    liga_id = serializers.IntegerField()
    usuario_id = serializers.IntegerField()
    posicion = serializers.IntegerField(allow_null=True)
    puntos = serializers.IntegerField(allow_null=True)
    porcentaje = serializers.FloatField(allow_null=True)
    monto_premio = serializers.FloatField()
    monto_total_liga = serializers.FloatField(allow_null=True)
    mensaje = serializers.CharField(required=False)


class ConfiguracionPremioSerializer(serializers.Serializer):
    """Serializador para configurar distribución de premios"""
    posicion = serializers.IntegerField()
    porcentaje = serializers.DecimalField(max_digits=5, decimal_places=2)
