from rest_framework import status

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import login, logout, get_user_model

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator



from .serializers import (

    UserSerializer, 

    RegisterSerializer, 

    LoginSerializer

)



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

    """Vista para login de usuarios"""

    permission_classes = [AllowAny]



    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data['user']

            # No usar login() de Django ya que el modelo no tiene last_login
            # login(request, user)

            return Response({

                'message': 'Login exitoso',

                'user': UserSerializer(user).data

            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LogoutView(APIView):

    """Vista para logout de usuarios"""

    permission_classes = [IsAuthenticated]



    def post(self, request):

        logout(request)

        return Response({

            'message': 'Logout exitoso'

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

