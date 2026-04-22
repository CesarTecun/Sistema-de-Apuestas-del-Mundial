from rest_framework import serializers
from .models import Liga, Invitacion

class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = '__all__'


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
