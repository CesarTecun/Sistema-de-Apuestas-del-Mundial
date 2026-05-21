from rest_framework import status

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import logout, get_user_model
from django.utils import timezone



from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    SessionTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from .utils import cerrar_sesion_usuario, obtener_sesiones_activas, generar_tokens_y_sesion
from .models import SesionUsuario
from .emails import enviar_correo_recuperacion



User = get_user_model()





class RegisterView(APIView):

    """Vista para registro de nuevos usuarios"""

    permission_classes = [AllowAny]



    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            return Response({

                'message': 'Usuario creado exitosamente',

                'user': UserSerializer(user).data

            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LoginView(APIView):
    """Vista para login de usuarios con seguimiento de sesión"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh, access, sesion = generar_tokens_y_sesion(user, request)
            
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
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass
        # Cerrar sesión en base de datos
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

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_obj = serializer.save()

        if token_obj:
            enviar_correo_recuperacion(token_obj)

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


class SessionTokenObtainPairView(TokenObtainPairView):
    serializer_class = SessionTokenObtainPairSerializer
