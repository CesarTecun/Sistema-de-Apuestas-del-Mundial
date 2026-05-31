from rest_framework import serializers
from .models import Pronostico

class PronosticoSerializer(serializers.ModelSerializer):
    resultado_display = serializers.ReadOnlyField()
    ganador_pronostico = serializers.ReadOnlyField()
    usuario_nombre = serializers.SerializerMethodField()
    usuario_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Pronostico
        fields = ['id_pronostico', 'fk_id_usuario', 'fk_id_partido', 'fk_id_liga', 
                  'gol_local', 'gol_visitante', 'puntos_obtenidos', 'resultado_display', 
                  'ganador_pronostico', 'usuario_nombre', 'usuario_email']
        read_only_fields = ('id_pronostico', 'fk_id_usuario', 'puntos_obtenidos')
    
    def get_usuario_nombre(self, obj):
        """Obtener el nombre completo del usuario"""
        try:
            from backend.usuarios.models import Usuario
            usuario = Usuario.objects.get(id_usuario=obj.fk_id_usuario)
            return usuario.get_full_name() or 'Usuario'
        except Usuario.DoesNotExist:
            return 'Usuario no encontrado'
    
    def get_usuario_email(self, obj):
        """Obtener el email del usuario"""
        try:
            from backend.usuarios.models import Usuario
            usuario = Usuario.objects.get(id_usuario=obj.fk_id_usuario)
            return usuario.email
        except Usuario.DoesNotExist:
            return None
    
    def validate(self, data):
        """Validación personalizada para los goles"""
        if data.get('gol_local', 0) < 0:
            raise serializers.ValidationError("Los goles del equipo local no pueden ser negativos")
        if data.get('gol_visitante', 0) < 0:
            raise serializers.ValidationError("Los goles del equipo visitante no pueden ser negativos")
        return data
    
    def validate_fk_id_partido(self, value):
        """Validar que el partido exista"""
        try:
            from backend.partidos.models import Partido
            Partido.objects.get(id_partido=value)
        except Partido.DoesNotExist:
            raise serializers.ValidationError("El partido especificado no existe")
        return value
    
    def validate_fk_id_liga(self, value):
        """Validar que la liga exista"""
        try:
            from backend.ligas.models import Liga
            Liga.objects.get(id_liga=value)
        except Liga.DoesNotExist:
            raise serializers.ValidationError("La liga especificada no existe")
        return value
