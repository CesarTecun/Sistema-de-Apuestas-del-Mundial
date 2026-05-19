from rest_framework import serializers
from .models import Partido, Jugador, Seleccion
from backend.core.models import Sede


class PartidoSerializer(serializers.ModelSerializer):
    resultado_display = serializers.ReadOnlyField()
    ganador = serializers.ReadOnlyField()
    ciudad_sede = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Partido
        fields = '__all__'
        read_only_fields = ('id_partido',)
        extra_kwargs = {
            'fk_id_liga': {'required': True},
        }

    def validate(self, data):
        """Validación personalizada para los goles y conversión de ciudad a sede"""
        if data.get('gol_local', 0) < 0:
            raise serializers.ValidationError("Los goles del equipo local no pueden ser negativos")
        if data.get('gol_visitante', 0) < 0:
            raise serializers.ValidationError("Los goles del equipo visitante no pueden ser negativos")
        if not data.get('fk_id_liga'):
            raise serializers.ValidationError({
                'fk_id_liga': 'Debes seleccionar la liga a la que pertenece el partido.'
            })
        
        # Convertir ciudad_sede a fk_sede si se proporciona
        ciudad_sede = data.pop('ciudad_sede', None)
        if ciudad_sede:
            try:
                sede = Sede.objects.filter(ciudad__iexact=ciudad_sede).first()
                if sede:
                    data['fk_sede'] = sede.id_sede
                else:
                    raise serializers.ValidationError({
                        'ciudad_sede': f'No existe una sede con la ciudad "{ciudad_sede}"'
                    })
            except Exception as e:
                raise serializers.ValidationError({
                    'ciudad_sede': f'Error al buscar la sede: {str(e)}'
                })
        
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
