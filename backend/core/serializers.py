from rest_framework import serializers
from .models import Sede, FaseGrupo, Bitacora, AuditLog, ConfiguracionTorneo


class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ['id_sede', 'ciudad', 'estadio']
        read_only_fields = ['id_sede']


class FaseGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaseGrupo
        fields = ['id_fase', 'nombre_fase']
        read_only_fields = ['id_fase']


class BitacoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = ['log', 'hora', 'fecha', 'detalle_accion', 'fk_id_usuario']
        read_only_fields = ['log', 'hora', 'fecha']


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            'id_audit_log', 'table_name', 'operation', 'record_pk',
            'old_data', 'new_data', 'changed_by', 'changed_at',
        ]
        read_only_fields = [
            'id_audit_log', 'table_name', 'operation', 'record_pk',
            'old_data', 'new_data', 'changed_by', 'changed_at',
        ]


class ConfiguracionTorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionTorneo
        fields = [
            'porcentaje_plataforma', 'puntos_exacto', 'puntos_ganador',
            'fecha_inicio_torneo', 'fecha_fin_torneo',
            'permite_registro_abierto', 'max_ligas_por_usuario',
        ]
