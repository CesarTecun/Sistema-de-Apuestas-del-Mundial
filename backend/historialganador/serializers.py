from rest_framework import serializers
from .models import HistorialGanador


class HistorialGanadorSerializer(serializers.ModelSerializer):
    """Serializador para el modelo HistorialGanador"""
    
    class Meta:
        model = HistorialGanador
        fields = ['id_pago', 'fk_id_usuario', 'fk_id_liga', 'monto_pagado', 'fecha_premio']
        read_only_fields = ('id_pago', 'fecha_premio')


class ResumenGanadorSerializer(serializers.Serializer):
    """Serializador para resumen de ganadores por liga"""
    liga_id = serializers.IntegerField()
    total_ganadores = serializers.IntegerField()
    monto_total_pagado = serializers.FloatField()
    ganadores = HistorialGanadorSerializer(many=True)
