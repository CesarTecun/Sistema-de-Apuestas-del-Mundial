from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from backend.utils.viewsets import SoftDeleteModelViewSet
from .models import Liga, Invitacion, ParticipanteLiga
from .serializers import LigaSerializer, InvitacionSerializer
from backend.ligas.serializers import ParticipanteLigaSerializer
from backend.usuarios.models import Usuario

class LigaViewSet(SoftDeleteModelViewSet):
    """
    API endpoint para gestionar ligas
    Permite operaciones CRUD completas
    """
    serializer_class = LigaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Solo mostrar ligas donde el usuario es admin, participante o tiene invitación"""
        user = self.request.user
        usuario_id = user.id_usuario
        
        # Ligas donde el usuario es administrador
        ligas_admin = Liga.objects.filter(fk_administrador=usuario_id)
        
        # Ligas donde el usuario es participante
        ligas_participante_ids = ParticipanteLiga.objects.filter(
            fk_id_usuario=usuario_id,
            estado_participacion='Activo'
        ).values_list('fk_id_liga', flat=True)
        ligas_participante = Liga.objects.filter(id_liga__in=ligas_participante_ids)
        
        # Ligas donde el usuario tiene invitación pendiente o aceptada
        ligas_invitacion_ids = Invitacion.objects.filter(
            fk_id_usuario_invitado=usuario_id,
            estado_invitacion__in=['Pendiente', 'Aceptada']
        ).values_list('fk_id_liga', flat=True)
        ligas_invitacion = Liga.objects.filter(id_liga__in=ligas_invitacion_ids)
        
        # Combinar todos los querysets y eliminar duplicados
        from django.db.models import Q
        queryset = ligas_admin | ligas_participante | ligas_invitacion
        return queryset.distinct()
    
    def create(self, request, *args, **kwargs):
        """Crear una nueva liga"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='enviar-invitacion')
    def enviar_invitacion(self, request, pk=None):
        """Enviar invitación a un usuario para unirse a la liga"""
        try:
            liga = self.get_object()
        except Liga.DoesNotExist:
            return Response({'error': 'Liga no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar que el usuario es administrador de la liga
        if liga.fk_administrador != request.user.id_usuario:
            return Response({'error': 'Solo el administrador puede enviar invitaciones'}, status=status.HTTP_403_FORBIDDEN)
        
        usuario_invitado_id = request.data.get('fk_id_usuario_invitado')
        if not usuario_invitado_id:
            return Response({'error': 'Se requiere el ID del usuario invitado'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que el usuario invitado existe
        try:
            usuario_invitado = Usuario.objects.get(id_usuario=usuario_invitado_id)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario invitado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar que no exista una invitación previa
        if Invitacion.objects.filter(
            fk_id_liga=liga.id_liga,
            fk_id_usuario_invitado=usuario_invitado_id,
            estado_invitacion__in=['Pendiente', 'Aceptada']
        ).exists():
            return Response({'error': 'Ya existe una invitación pendiente o aceptada para este usuario'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear la invitación
        invitacion = Invitacion.objects.create(
            fk_id_liga=liga.id_liga,
            fk_id_usuario_invitado=usuario_invitado_id,
            fk_id_usuario_administrador=request.user.id_usuario,
            email_invitado=request.data.get('email_invitado', usuario_invitado.email),
            mensaje_invitacion=request.data.get('mensaje_invitacion', '')
        )
        
        serializer = InvitacionSerializer(invitacion)
        return Response({
            'message': 'Invitación enviada exitosamente',
            'invitacion': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        """Obtener una liga específica"""
        try:
            liga = self.get_object()
            serializer = self.get_serializer(liga)
            return Response(serializer.data)
        except Liga.DoesNotExist:
            return Response({'error': 'Liga no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Actualizar una liga existente"""
        try:
            liga = self.get_object()
            serializer = self.get_serializer(liga, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Liga.DoesNotExist:
            return Response({'error': 'Liga no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        """Eliminar una liga"""
        try:
            liga = self.get_object()
            liga.delete()
            return Response({'message': 'Liga eliminada correctamente'}, status=status.HTTP_200_OK)
        except Liga.DoesNotExist:
            return Response({'error': 'Liga no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ligas_por_usuario(request):
    """Obtener ligas administradas por un usuario específico"""
    usuario_id = request.query_params.get('usuario_id')
    if not usuario_id:
        return Response({'error': 'Se requiere el ID del usuario'}, status=status.HTTP_400_BAD_REQUEST)
    
    ligas = Liga.objects.filter(fk_administrador=usuario_id)
    serializer = LigaSerializer(ligas, many=True)
    return Response(serializer.data)


class ParticipanteLigaViewSet(SoftDeleteModelViewSet):
    """
    API endpoint para gestionar participantes de ligas.
    Implementa soft delete - al "eliminar" solo cambia status a False.
    """
    queryset = ParticipanteLiga.objects.all()
    serializer_class = ParticipanteLigaSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id_participante'


class InvitacionViewSet(SoftDeleteModelViewSet):
    """
    API endpoint para gestionar invitaciones a ligas.
    Implementa soft delete - al "eliminar" solo cambia status a False.
    """
    serializer_class = InvitacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id_invitacion'
    
    def get_queryset(self):
        """Solo mostrar invitaciones del usuario actual"""
        user = self.request.user
        return Invitacion.objects.filter(fk_id_usuario_invitado=user.id_usuario)
    
    @action(detail=True, methods=['post'], url_path='aceptar')
    def aceptar(self, request, pk=None):
        """Aceptar una invitación y unirse a la liga"""
        try:
            invitacion = self.get_object()
        except Invitacion.DoesNotExist:
            return Response({'error': 'Invitación no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        if invitacion.estado_invitacion != 'Pendiente':
            return Response({'error': 'Esta invitación ya no está pendiente'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar estado de la invitación
        invitacion.estado_invitacion = 'Aceptada'
        invitacion.save()
        
        # Crear registro de participante en la liga
        ParticipanteLiga.objects.create(
            fk_id_liga=invitacion.fk_id_liga,
            fk_id_usuario=request.user.id_usuario,
            estado_participacion='Activo'
        )
        
        return Response({
            'message': 'Invitación aceptada exitosamente',
            'invitacion': InvitacionSerializer(invitacion).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='rechazar')
    def rechazar(self, request, pk=None):
        """Rechazar una invitación"""
        try:
            invitacion = self.get_object()
        except Invitacion.DoesNotExist:
            return Response({'error': 'Invitación no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        if invitacion.estado_invitacion != 'Pendiente':
            return Response({'error': 'Esta invitación ya no está pendiente'}, status=status.HTTP_400_BAD_REQUEST)
        
        invitacion.estado_invitacion = 'Rechazada'
        invitacion.save()
        
        return Response({
            'message': 'Invitación rechazada',
            'invitacion': InvitacionSerializer(invitacion).data
        }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        """Crear una nueva invitación (envía correo automáticamente si tiene email)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitacion = serializer.save()
        
        # Enviar correo si se proporcionó email
        if invitacion.email_invitado:
            try:
                self.enviar_email_invitacion(invitacion)
                return Response({
                    'invitacion': serializer.data,
                    'email_enviado': True,
                    'message': 'Invitación creada y correo enviado exitosamente'
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'invitacion': serializer.data,
                    'email_enviado': False,
                    'error': str(e),
                    'message': 'Invitación creada pero hubo error al enviar correo'
                }, status=status.HTTP_201_CREATED)
        
        return Response({
            'invitacion': serializer.data,
            'email_enviado': False,
            'message': 'Invitación creada (sin correo - no se proporcionó email)'
        }, status=status.HTTP_201_CREATED)
    
    def enviar_email_invitacion(self, invitacion):
        """Método auxiliar para enviar correo de invitación"""
        asunto = '🏆 Has sido invitado a una Liga de la Copa Mundial FIFA 2026'
        
        mensaje = f"""
¡Hola!

Has sido invitado a unirte a una liga en nuestro sistema de pronósticos para la Copa Mundial FIFA 2026.

📋 Detalles de la invitación:
• ID de Liga: {invitacion.fk_id_liga}
• Estado: {invitacion.estado_invitacion}

💬 Mensaje del administrador:
{invitacion.mensaje_invitacion or 'Sin mensaje personalizado'}

🔗 Para aceptar la invitación, por favor inicia sesión en tu cuenta o regístrate si aún no tienes una en:
http://localhost:3000/invitaciones/{invitacion.id_invitacion}

¡Que gane el mejor!

---
Copa Mundial FIFA 2026 - Sistema de Pronósticos
Este es un correo automático, por favor no respondas a este mensaje.
        """
        
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitacion.email_invitado],
            fail_silently=False,
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enviar_invitacion_email_api(request):
    """
    Endpoint para enviar correo de invitación manualmente
    POST /api/ligas/invitaciones/<id>/enviar-email/
    """
    invitacion_id = request.data.get('invitacion_id')
    
    if not invitacion_id:
        return Response(
            {'error': 'Se requiere invitacion_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        invitacion = Invitacion.objects.get(id_invitacion=invitacion_id)
        
        if not invitacion.email_invitado:
            return Response(
                {'error': 'La invitación no tiene email asociado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        asunto = '🏆 Has sido invitado a una Liga de la Copa Mundial FIFA 2026'
        
        mensaje = f"""
¡Hola!

Has sido invitado a unirte a una liga en nuestro sistema de pronósticos para la Copa Mundial FIFA 2026.

📋 Detalles de la invitación:
• ID de Liga: {invitacion.fk_id_liga}
• Estado: {invitacion.estado_invitacion}

💬 Mensaje del administrador:
{invitacion.mensaje_invitacion or 'Sin mensaje personalizado'}

🔗 Para aceptar la invitación, por favor inicia sesión en tu cuenta o regístrate si aún no tienes una.

¡Que gane el mejor!

---
Copa Mundial FIFA 2026 - Sistema de Pronósticos
Este es un correo automático, por favor no respondas a este mensaje.
        """
        
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitacion.email_invitado],
            fail_silently=False,
        )
        
        return Response({
            'message': f'Correo enviado exitosamente a {invitacion.email_invitado}'
        })
        
    except Invitacion.DoesNotExist:
        return Response(
            {'error': 'Invitación no encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Error al enviar correo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
