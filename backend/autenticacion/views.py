from rest_framework import status

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from django.contrib.auth import logout, get_user_model
from django.utils import timezone
import hashlib
import secrets
from datetime import timedelta


from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    SessionTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
    EmailVerificationSerializer,
)
from .utils import cerrar_sesion_usuario, obtener_sesiones_activas, generar_tokens_y_sesion
from .models import SesionUsuario, EmailVerificationToken
from .emails import enviar_correo_recuperacion, enviar_correo_verificacion
from backend.utils.bitacora import registrar_bitacora



User = get_user_model()





class RegisterView(APIView):
    """Vista para registro de nuevos usuarios con verificación de email."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            registrar_bitacora(user.id_usuario, f'Registro de nuevo usuario: {user.email}')

            # Generar token de verificación de email (hash en BD)
            token_plano = secrets.token_hex(32)
            token_hash = hashlib.sha256(token_plano.encode()).hexdigest()
            EmailVerificationToken.objects.create(
                usuario=user,
                token_hash=token_hash,
                expires_at=timezone.now() + timedelta(hours=24)
            )
            enviar_correo_verificacion(user, token_plano)

            return Response({
                'message': 'Usuario creado exitosamente. Revisa tu email para activar tu cuenta.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LoginView(APIView):
    """Vista para login de usuarios con seguimiento de sesión"""
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='5/5m', method='POST', block=False))
    def post(self, request):
        if getattr(request, 'limited', False):
            return Response(
                {'detail': 'Demasiados intentos fallidos de inicio de sesión. Por favor, inténtalo de nuevo más tarde.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh, access, sesion = generar_tokens_y_sesion(user, request)
            registrar_bitacora(user.id_usuario, f'Inicio de sesión: {user.email}')

            # Preparar respuesta con info de sesión
            response_data = {
                'message': 'Login exitoso',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': access,
                    'refresh': refresh,
                },
                'sesion': {
                    'id_sesion': sesion.id_sesion if sesion else None,
                    'token_sesion': sesion.token_sesion if sesion else None,
                    'dispositivo': sesion.dispositivo if sesion else None,
                    'ip_address': sesion.ip_address if sesion else None,
                } if sesion else None
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LogoutView(APIView):
    """Vista para logout de usuarios con cierre de sesión en BD"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        registrar_bitacora(request.user.id_usuario, f'Cierre de sesión: {request.user.email}')

        # Cerrar sesión en base de datos (marca todas las sesiones activas del usuario)
        cerrar_sesion_usuario(request, refresh_token=refresh_token)

        # Logout de Django
        logout(request)

        return Response({
            'message': 'Logout exitoso',
            'sesion_cerrada': True
        }, status=status.HTTP_200_OK)





class UserProfileView(APIView):

    """Vista para obtener información del usuario actual"""

    permission_classes = [IsAuthenticated]



    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)



    def put(self, request):

        serializer = UserSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response({

                'message': 'Perfil actualizado',

                'user': serializer.data

            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CheckAuthView(APIView):

    """Vista para verificar si el usuario está autenticado"""

    permission_classes = [AllowAny]



    def get(self, request):

        if request.user.is_authenticated:

            return Response({

                'is_authenticated': True,

                'user': UserSerializer(request.user).data

            })

        return Response({
            'is_authenticated': False,
            'user': None
        })


class SesionesActivasView(APIView):
    """Vista para consultar sesiones activas del usuario"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todas las sesiones activas del usuario actual"""
        sesiones = obtener_sesiones_activas(request.user.id_usuario)
        
        data = [{
            'id_sesion': s.id_sesion,
            'token_sesion': s.token_sesion[:20] + '...' if s.token_sesion else None,  # Truncado por seguridad
            'fecha_inicio': s.fecha_inicio,
            'fecha_ultima_actividad': s.fecha_ultima_actividad,
            'dispositivo': s.dispositivo,
            'ip_address': s.ip_address,
            'estado_sesion': s.estado_sesion,
            'is_sesion_actual': s.token_sesion == request.session.get('token_sesion')
        } for s in sesiones]
        
        return Response({
            'sesiones_activas': data,
            'total': len(data)
        })


class CerrarSesionView(APIView):
    """Vista para cerrar una sesión específica por ID"""
    permission_classes = [IsAuthenticated]

    def post(self, request, sesion_id):
        """Cierra una sesión específica del usuario"""
        try:
            sesion = SesionUsuario.objects.get(
                id_sesion=sesion_id,
                fk_id_usuario=request.user.id_usuario
            )
            
            # No permitir cerrar la sesión actual por este endpoint (usar logout)
            if sesion.token_sesion == request.session.get('token_sesion'):
                return Response({
                    'error': 'Use el endpoint de logout para cerrar la sesión actual'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            sesion.estado_sesion = 'Cerrada'
            sesion.fecha_cierre = timezone.now()
            sesion.save(update_fields=['estado_sesion', 'fecha_cierre'])
            
            return Response({
                'message': 'Sesión cerrada exitosamente',
                'id_sesion': sesion_id
            })
            
        except SesionUsuario.DoesNotExist:
            return Response({
                'error': 'Sesión no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='3/10m', method='POST', block=False))
    def post(self, request):
        if getattr(request, 'limited', False):
            return Response(
                {'detail': 'Demasiados intentos de recuperación de contraseña. Por favor, inténtalo de nuevo más tarde.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_obj, token_plano = serializer.save()

        if token_obj:
            enviar_correo_recuperacion(token_obj.usuario, token_plano)

        return Response({
            'message': 'Si el correo existe, recibirás instrucciones para restablecer la contraseña.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Contraseña actualizada correctamente.'})


class ChangePasswordView(APIView):
    """Vista para cambiar contraseña del usuario autenticado."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Contraseña actualizada correctamente. Todas tus sesiones han sido cerradas.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """Vista para verificar el email tras registro mediante token."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Email verificado correctamente. Ya puedes iniciar sesión.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionTokenObtainPairView(TokenObtainPairView):
    serializer_class = SessionTokenObtainPairSerializer
