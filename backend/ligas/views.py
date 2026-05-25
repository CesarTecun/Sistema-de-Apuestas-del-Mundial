from django.db.models import Q, Count, OuterRef, Subquery, IntegerField, F
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.utils.viewsets import SoftDeleteModelViewSet
from backend.autenticacion.serializers import RegisterSerializer, UserSerializer
from .models import Liga, Invitacion, ParticipanteLiga, SolicitudParticipacion
from .serializers import (
    LigaSerializer,
    InvitacionSerializer,
    ParticipanteLigaSerializer,
    SolicitudParticipacionSerializer,
)
from backend.usuarios.models import Usuario
from .emails import enviar_correo_invitacion


def contar_participantes_activos(liga_id: int) -> int:
    return ParticipanteLiga.objects.filter(
        fk_id_liga=liga_id,
        estado_participacion='Activo'
    ).count()


def hay_cupo_disponible(liga: Liga) -> bool:
    if liga.cupo_maximo is None:
        return True
    return contar_participantes_activos(liga.id_liga) < liga.cupo_maximo


def agregar_participante_a_liga(liga: Liga, usuario_id: int) -> ParticipanteLiga:
    participante, _ = ParticipanteLiga.objects.get_or_create(
        fk_id_liga=liga.id_liga,
        fk_id_usuario=usuario_id,
        defaults={'estado_participacion': 'Activo'}
    )
    participante.estado_participacion = 'Activo'
    participante.save(update_fields=['estado_participacion'])
    return participante

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
        
        # Ligas donde el usuario tiene invitación aceptada
        ligas_invitacion_ids = Invitacion.objects.filter(
            Q(fk_id_usuario_invitado=usuario_id) | Q(email_invitado__iexact=user.email),
            estado_invitacion='Aceptada'
        ).values_list('fk_id_liga', flat=True)
        ligas_invitacion = Liga.objects.filter(id_liga__in=ligas_invitacion_ids)
        
        # Combinar todos los querysets y eliminar duplicados
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
        email_invitado = request.data.get('email_invitado')
        usuario_invitado = None

        if usuario_invitado_id:
            try:
                usuario_invitado = Usuario.objects.get(id_usuario=usuario_invitado_id)
            except Usuario.DoesNotExist:
                return Response({'error': 'Usuario invitado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        elif email_invitado:
            try:
                usuario_invitado = Usuario.objects.get(email__iexact=email_invitado)
                usuario_invitado_id = usuario_invitado.id_usuario
            except Usuario.DoesNotExist:
                usuario_invitado = None

        if not usuario_invitado_id and not email_invitado:
            return Response({'error': 'Debes indicar el correo del invitado si aún no está registrado'}, status=status.HTTP_400_BAD_REQUEST)

        if usuario_invitado and not email_invitado:
            email_invitado = usuario_invitado.email

        if not email_invitado:
            return Response({'error': 'No se pudo determinar el correo del invitado'}, status=status.HTTP_400_BAD_REQUEST)

        invitacion_existente = Invitacion.objects.filter(
            fk_id_liga=liga.id_liga,
            estado_invitacion__in=['Pendiente', 'Aceptada']
        )
        if usuario_invitado_id:
            invitacion_existente = invitacion_existente.filter(fk_id_usuario_invitado=usuario_invitado_id)
        else:
            invitacion_existente = invitacion_existente.filter(email_invitado__iexact=email_invitado)

        if invitacion_existente.exists():
            return Response({'error': 'Ya existe una invitación pendiente para este usuario/correo'}, status=status.HTTP_400_BAD_REQUEST)

        invitacion = Invitacion.objects.create(
            fk_id_liga=liga.id_liga,
            fk_id_usuario_invitado=usuario_invitado_id,
            fk_id_usuario_administrador=request.user.id_usuario,
            email_invitado=email_invitado,
            mensaje_invitacion=request.data.get('mensaje_invitacion', '')
        )

        correo_enviado = False
        error_correo = None
        if invitacion.email_invitado:
            try:
                enviar_correo_invitacion(invitacion)
                correo_enviado = True
            except Exception as exc:
                error_correo = str(exc)
        
        serializer = InvitacionSerializer(invitacion)
        respuesta = {
            'message': 'Invitación creada',
            'invitacion': serializer.data,
            'email_enviado': correo_enviado,
        }
        if error_correo:
            respuesta['error_email'] = error_correo
        return Response(respuesta, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='solicitar-ingreso')
    def solicitar_ingreso(self, request, pk=None):
        """Permitir que un usuario solicite unirse a una liga pública."""
        try:
            liga = self.get_object()
        except Liga.DoesNotExist:
            return Response({'error': 'Liga no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        if not liga.es_publica:
            return Response({'error': 'Esta liga no acepta solicitudes públicas.'}, status=status.HTTP_400_BAD_REQUEST)

        if ParticipanteLiga.objects.filter(
            fk_id_liga=liga.id_liga,
            fk_id_usuario=request.user.id_usuario,
            estado_participacion='Activo'
        ).exists():
            return Response({'message': 'Ya eres participante de esta liga.'}, status=status.HTTP_200_OK)

        if not hay_cupo_disponible(liga):
            return Response({'error': 'La liga ya alcanzó su cupo máximo.'}, status=status.HTTP_400_BAD_REQUEST)

        if not liga.requiere_aprobacion:
            participante = agregar_participante_a_liga(liga, request.user.id_usuario)
            return Response({
                'message': 'Te uniste a la liga exitosamente.',
                'participante': ParticipanteLigaSerializer(participante).data,
                'aprobacion_requerida': False
            }, status=status.HTTP_200_OK)

        solicitud, created = SolicitudParticipacion.objects.get_or_create(
            liga=liga,
            usuario=request.user,
            estado='Pendiente',
            defaults={
                'email_contacto': request.user.email,
                'mensaje': request.data.get('mensaje', ''),
            }
        )

        if not created:
            solicitud.email_contacto = request.user.email
            solicitud.mensaje = request.data.get('mensaje', solicitud.mensaje)
            solicitud.save(update_fields=['email_contacto', 'mensaje'])

        serializer = SolicitudParticipacionSerializer(solicitud)
        return Response({
            'message': 'Solicitud enviada. El administrador revisará tu petición.',
            'solicitud': serializer.data,
            'aprobacion_requerida': True
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
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


# ---------- Solicitudes de participación ----------

class SolicitudParticipacionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SolicitudParticipacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id_solicitud'

    def get_queryset(self):
        user = self.request.user
        estado = self.request.query_params.get('estado')
        queryset = SolicitudParticipacion.objects.select_related('liga', 'usuario').filter(
            Q(liga__fk_administrador=user.id_usuario) | Q(usuario=user)
        )
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    def _ensure_admin(self, solicitud: SolicitudParticipacion, user_id: int):
        if solicitud.liga.fk_administrador != user_id:
            raise PermissionError('Solo el administrador de la liga puede gestionar solicitudes.')

    @action(detail=True, methods=['post'], url_path='aprobar')
    def aprobar(self, request, id_solicitud=None):
        try:
            solicitud = self.get_object()
            self._ensure_admin(solicitud, request.user.id_usuario)
        except PermissionError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_403_FORBIDDEN)

        if solicitud.estado != 'Pendiente':
            return Response({'error': 'La solicitud ya fue gestionada.'}, status=status.HTTP_400_BAD_REQUEST)

        if not hay_cupo_disponible(solicitud.liga):
            return Response({'error': 'La liga ya no tiene cupos disponibles.'}, status=status.HTTP_400_BAD_REQUEST)

        participante = agregar_participante_a_liga(solicitud.liga, solicitud.usuario.id_usuario)

        solicitud.estado = 'Aprobada'
        solicitud.fecha_respuesta = timezone.now()
        solicitud.respondido_por = request.user.id_usuario
        solicitud.respuesta_admin = request.data.get('respuesta_admin', '')
        solicitud.save(update_fields=['estado', 'fecha_respuesta', 'respondido_por', 'respuesta_admin'])

        return Response({
            'message': 'Solicitud aprobada y participante agregado.',
            'solicitud': SolicitudParticipacionSerializer(solicitud).data,
            'participante': ParticipanteLigaSerializer(participante).data,
        })

    @action(detail=True, methods=['post'], url_path='rechazar')
    def rechazar(self, request, id_solicitud=None):
        try:
            solicitud = self.get_object()
            self._ensure_admin(solicitud, request.user.id_usuario)
        except PermissionError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_403_FORBIDDEN)

        if solicitud.estado != 'Pendiente':
            return Response({'error': 'La solicitud ya fue gestionada.'}, status=status.HTTP_400_BAD_REQUEST)

        solicitud.estado = 'Rechazada'
        solicitud.fecha_respuesta = timezone.now()
        solicitud.respondido_por = request.user.id_usuario
        solicitud.respuesta_admin = request.data.get('respuesta_admin', '')
        solicitud.save(update_fields=['estado', 'fecha_respuesta', 'respondido_por', 'respuesta_admin'])

        return Response({
            'message': 'Solicitud rechazada.',
            'solicitud': SolicitudParticipacionSerializer(solicitud).data,
        })


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
        return Invitacion.objects.filter(
            Q(fk_id_usuario_invitado=user.id_usuario) | Q(email_invitado__iexact=user.email)
        )
    
    @action(detail=True, methods=['post'], url_path='aceptar')
    def aceptar(self, request, pk=None):
        """Aceptar una invitación y unirse a la liga"""
        try:
            invitacion = self.get_object()
        except Invitacion.DoesNotExist:
            return Response({'error': 'Invitación no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        if invitacion.estado_invitacion != 'Pendiente':
            return Response({'error': 'Esta invitación ya no está pendiente'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que la invitación corresponde al usuario
        if invitacion.email_invitado and invitacion.email_invitado.lower() != request.user.email.lower():
            return Response({'error': 'Esta invitación pertenece a otro correo'}, status=status.HTTP_403_FORBIDDEN)

        if invitacion.fk_id_usuario_invitado is None:
            invitacion.fk_id_usuario_invitado = request.user.id_usuario

        # Actualizar estado de la invitación
        invitacion.estado_invitacion = 'Aceptada'
        invitacion.save(update_fields=['estado_invitacion', 'fk_id_usuario_invitado'])
        
        # Crear registro de participante en la liga
        if not ParticipanteLiga.objects.filter(
            fk_id_liga=invitacion.fk_id_liga,
            fk_id_usuario=request.user.id_usuario
        ).exists():
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
        
        if invitacion.email_invitado and invitacion.email_invitado.lower() != request.user.email.lower():
            return Response({'error': 'Esta invitación pertenece a otro correo'}, status=status.HTTP_403_FORBIDDEN)
        
        if invitacion.fk_id_usuario_invitado and invitacion.fk_id_usuario_invitado != request.user.id_usuario:
            return Response({'error': 'Esta invitación pertenece a otro usuario'}, status=status.HTTP_403_FORBIDDEN)
        
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
                enviar_correo_invitacion(invitacion)
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
        
        enviar_correo_invitacion(invitacion)
        
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


class LigasPublicasView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        search = request.query_params.get('search')
        tipo = request.query_params.get('tipo')
        disponibles = request.query_params.get('disponibles')
        requiere_aprobacion = request.query_params.get('requiere_aprobacion')

        participantes_subquery = ParticipanteLiga.objects.filter(
            fk_id_liga=OuterRef('id_liga'),
            estado_participacion='Activo'
        ).values('fk_id_liga').annotate(total=Count('id_participante')).values('total')

        queryset = Liga.objects.filter(status=True, es_publica=True).annotate(
            total_participantes=Coalesce(
                Subquery(participantes_subquery, output_field=IntegerField()),
                0
            )
        )

        if search:
            queryset = queryset.filter(
                Q(nombre_liga__icontains=search) |
                Q(descripcion__icontains=search)
            )

        if tipo:
            queryset = queryset.filter(tipo_liga=tipo)

        if requiere_aprobacion in ['true', 'false']:
            queryset = queryset.filter(requiere_aprobacion=(requiere_aprobacion == 'true'))

        if disponibles == 'true':
            queryset = queryset.filter(
                Q(cupo_maximo__isnull=True) |
                Q(cupo_maximo__gt=F('total_participantes'))
            )

        serializer = LigaSerializer(queryset.order_by('nombre_liga'), many=True)
        return Response({'results': serializer.data})


class InvitacionPublicaView(APIView):
    permission_classes = [AllowAny]

    def _get_invitacion(self, codigo):
        return get_object_or_404(Invitacion, codigo_invitacion=codigo)

    def _get_liga(self, invitacion):
        return Liga.objects.filter(id_liga=invitacion.fk_id_liga, status=True).first()

    def get(self, request, codigo):
        invitacion = self._get_invitacion(codigo)
        liga = self._get_liga(invitacion)
        liga_data = LigaSerializer(liga).data if liga else None
        return Response({
            'id_invitacion': invitacion.id_invitacion,
            'estado': invitacion.estado_invitacion,
            'email_invitado': invitacion.email_invitado,
            'liga': liga_data,
        })

    def post(self, request, codigo):
        invitacion = self._get_invitacion(codigo)
        liga = self._get_liga(invitacion)

        if not liga:
            return Response({'error': 'La liga asociada a esta invitación no está disponible.'}, status=status.HTTP_404_NOT_FOUND)

        if invitacion.estado_invitacion != 'Pendiente':
            return Response({'error': 'Esta invitación ya fue gestionada.'}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email') or invitacion.email_invitado
        if not email:
            return Response({'error': 'Debes proporcionar un correo electrónico.'}, status=status.HTTP_400_BAD_REQUEST)

        if invitacion.email_invitado and invitacion.email_invitado.lower() != email.lower():
            return Response({'error': 'El correo proporcionado no coincide con el de la invitación.'}, status=status.HTTP_400_BAD_REQUEST)

        usuario = None
        if invitacion.fk_id_usuario_invitado:
            usuario = Usuario.objects.filter(id_usuario=invitacion.fk_id_usuario_invitado).first()

        if not usuario:
            try:
                usuario = Usuario.objects.get(email__iexact=email)
            except Usuario.DoesNotExist:
                register_data = request.data.copy()
                register_data['email'] = email
                serializer = RegisterSerializer(data=register_data)
                serializer.is_valid(raise_exception=True)
                usuario = serializer.save()

        if not hay_cupo_disponible(liga):
            return Response({'error': 'La liga ya alcanzó su cupo máximo.'}, status=status.HTTP_400_BAD_REQUEST)

        participante = agregar_participante_a_liga(liga, usuario.id_usuario)

        invitacion.fk_id_usuario_invitado = usuario.id_usuario
        invitacion.estado_invitacion = 'Aceptada'
        invitacion.save(update_fields=['estado_invitacion', 'fk_id_usuario_invitado'])

        return Response({
            'message': 'Invitación aceptada. Usuario vinculado y agregado a la liga.',
            'liga': LigaSerializer(liga).data,
            'usuario': UserSerializer(usuario).data,
            'participante': ParticipanteLigaSerializer(participante).data,
        }, status=status.HTTP_201_CREATED)
