from rest_framework import serializers

from .models import Liga, Invitacion, ParticipanteLiga, SolicitudParticipacion


class LigaSerializer(serializers.ModelSerializer):
    total_participantes = serializers.SerializerMethodField()
    cupos_disponibles = serializers.SerializerMethodField()

    class Meta:
        model = Liga
        fields = '__all__'

    def get_total_participantes(self, obj):
        annotated = getattr(obj, 'total_participantes', None)
        if annotated is not None:
            return annotated

        return ParticipanteLiga.objects.filter(
            fk_id_liga=obj.id_liga,
            estado_participacion='Activo'
        ).count()

    def get_cupos_disponibles(self, obj):
        if obj.cupo_maximo is None:
            return None

        total = self.get_total_participantes(obj)
        restantes = obj.cupo_maximo - total
        return restantes if restantes >= 0 else 0



class ParticipanteLigaSerializer(serializers.ModelSerializer):
    """Serializer para gestionar participantes de ligas"""

    class Meta:
        model = ParticipanteLiga
        fields = [
            'id_participante',
            'fk_id_liga',
            'fk_id_usuario',
            'fecha_union',
            'estado_participacion',
            'status'
        ]
        read_only_fields = ['id_participante', 'fecha_union']


class InvitacionSerializer(serializers.ModelSerializer):
    """Serializer para crear y gestionar invitaciones"""

    class Meta:
        model = Invitacion
        fields = [
            'id_invitacion',
            'fk_id_liga',
            'codigo_invitacion',
            'fk_id_usuario_invitado',
            'fk_id_usuario_administrador',
            'email_invitado',
            'mensaje_invitacion',
            'estado_invitacion',
            'fecha_invitacion'
        ]
        read_only_fields = ['id_invitacion', 'codigo_invitacion', 'fecha_invitacion', 'estado_invitacion']

    def validate(self, attrs):
        email = attrs.get('email_invitado')
        usuario_id = attrs.get('fk_id_usuario_invitado')

        if not usuario_id and not email:
            raise serializers.ValidationError({
                'email_invitado': 'Debes proporcionar el correo del invitado si aún no existe en el sistema.'
            })

        return attrs


class SolicitudParticipacionSerializer(serializers.ModelSerializer):
    liga_nombre = serializers.CharField(source='liga.nombre_liga', read_only=True)
    tipo_liga = serializers.CharField(source='liga.tipo_liga', read_only=True)

    class Meta:
        model = SolicitudParticipacion
        fields = [
            'id_solicitud',
            'liga',
            'liga_nombre',
            'tipo_liga',
            'usuario',
            'email_contacto',
            'mensaje',
            'estado',
            'respuesta_admin',
            'fecha_solicitud',
            'fecha_respuesta',
            'respondido_por',
        ]
        read_only_fields = [
            'id_solicitud',
            'liga_nombre',
            'tipo_liga',
            'estado',
            'respuesta_admin',
            'fecha_solicitud',
            'fecha_respuesta',
            'respondido_por',
        ]
