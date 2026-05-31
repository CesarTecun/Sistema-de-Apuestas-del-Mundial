from rest_framework import serializers

from django.db.models import Sum, F, Window, IntegerField

from django.db.models.functions import Rank



from .models import Liga, Invitacion, ParticipanteLiga, SolicitudParticipacion

from backend.usuarios.models import Usuario





class LigaSerializer(serializers.ModelSerializer):

    total_participantes = serializers.SerializerMethodField()

    cupos_disponibles = serializers.SerializerMethodField()



    class Meta:

        model = Liga

        fields = '__all__'

        read_only_fields = ['updated_at', 'updated_by', 'deleted_by']



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



    def update(self, instance, validated_data):

        # Registrar el usuario que está haciendo la modificación

        request = self.context.get('request')

        if request and hasattr(request, 'user') and hasattr(request.user, 'id_usuario'):

            validated_data['updated_by'] = request.user.id_usuario

        return super().update(instance, validated_data)







class ParticipanteLigaSerializer(serializers.ModelSerializer):

    """Serializer para gestionar participantes de ligas"""

    usuario_nombre = serializers.SerializerMethodField()

    usuario_email = serializers.SerializerMethodField()

    puntos_totales = serializers.SerializerMethodField()

    posicion_ranking = serializers.SerializerMethodField()



    class Meta:

        model = ParticipanteLiga

        fields = [

            'id_participante',

            'fk_id_liga',

            'fk_id_usuario',

            'usuario_nombre',

            'usuario_email',

            'fecha_union',

            'estado_participacion',

            'puntos_totales',

            'posicion_ranking',

            'updated_at',

            'updated_by',

            'deleted_by'

        ]

        read_only_fields = ['id_participante', 'fecha_union', 'updated_at', 'updated_by', 'deleted_by']



    def get_usuario_nombre(self, obj):

        try:

            usuario = Usuario.objects.get(id_usuario=obj.fk_id_usuario)

            return f"{usuario.primer_nombre} {usuario.primer_apellido}"

        except Usuario.DoesNotExist:

            return "Usuario no encontrado"



    def get_usuario_email(self, obj):

        try:

            usuario = Usuario.objects.get(id_usuario=obj.fk_id_usuario)

            return usuario.email

        except Usuario.DoesNotExist:

            return None



    def get_puntos_totales(self, obj):

        """Obtener los puntos totales del usuario en la liga (anotados en el queryset)"""

        # Usar los puntos anotados en el queryset si están disponibles

        if hasattr(obj, 'puntos_totales') and obj.puntos_totales is not None:

            return obj.puntos_totales

        # Fallback: calcular los puntos si no están anotados

        try:

            from backend.pronosticos.models import Pronostico

            puntos = Pronostico.objects.filter(

                fk_id_usuario=obj.fk_id_usuario,

                fk_id_liga=obj.fk_id_liga

            ).aggregate(total=Sum('puntos_obtenidos'))['total'] or 0

            return puntos

        except Exception:

            return 0



    def get_posicion_ranking(self, obj):

        """Calcular la posición en el ranking de la liga"""

        try:

            from backend.pronosticos.models import Pronostico

            from django.db.models import OuterRef, Subquery



            # Usar la misma lógica de ordenamiento que la vista

            puntos_subquery = Pronostico.objects.filter(

                fk_id_usuario=OuterRef('fk_id_usuario'),

                fk_id_liga=OuterRef('fk_id_liga')

            ).values('fk_id_usuario').annotate(

                total=Sum('puntos_obtenidos')

            ).values('total')[:1]



            participantes_ordenados = ParticipanteLiga.objects.filter(

                fk_id_liga=obj.fk_id_liga,

                estado_participacion='Activo'

            ).annotate(

                puntos_totales=Subquery(puntos_subquery, output_field=models.IntegerField())

            ).order_by('-puntos_totales', 'fecha_union')



            # Encontrar la posición del usuario actual

            posicion = 1

            for p in participantes_ordenados:

                if p.fk_id_usuario == obj.fk_id_usuario:

                    return posicion

                posicion += 1



            return posicion

        except Exception:

            return 0



    def update(self, instance, validated_data):

        # Registrar el usuario que está haciendo la modificación

        request = self.context.get('request')

        if request and hasattr(request, 'user') and hasattr(request.user, 'id_usuario'):

            validated_data['updated_by'] = request.user.id_usuario

        return super().update(instance, validated_data)





class InvitacionSerializer(serializers.ModelSerializer):

    """Serializer para crear y gestionar invitaciones"""

    liga_nombre = serializers.SerializerMethodField()



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

            'fecha_invitacion',

            'liga_nombre'

        ]

        read_only_fields = ['id_invitacion', 'codigo_invitacion', 'fecha_invitacion', 'estado_invitacion']



    def get_liga_nombre(self, obj):

        if not obj.fk_id_liga:

            return "Liga no especificada"

        try:

            liga = Liga.objects.get(id_liga=obj.fk_id_liga)

            return liga.nombre_liga if liga.nombre_liga else "Sin nombre"

        except Liga.DoesNotExist:

            return "Liga eliminada"

        except Exception as e:

            return "Error"



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

