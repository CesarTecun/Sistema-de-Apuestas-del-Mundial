from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Liga, Invitacion
from .serializers import LigaSerializer, InvitacionSerializer

class LigaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar ligas
    Permite operaciones CRUD completas
    """
    queryset = Liga.objects.all()
    serializer_class = LigaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Crear una nueva liga"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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


class InvitacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar invitaciones a ligas
    """
    queryset = Invitacion.objects.all()
    serializer_class = InvitacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
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
