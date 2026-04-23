from rest_framework import serializers
from .models import Liga, Invitacion, ParticipanteLiga


class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = '__all__'


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
            'fk_id_usuario_invitado',
            'fk_id_usuario_administrador',
            'email_invitado',
            'mensaje_invitacion',
            'estado_invitacion',
            'fecha_invitacion'
        ]
        read_only_fields = ['id_invitacion', 'fecha_invitacion', 'estado_invitacion']
