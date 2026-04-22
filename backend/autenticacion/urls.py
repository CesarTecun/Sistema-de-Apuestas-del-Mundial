from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    CheckAuthView,
    SesionesActivasView,
    CerrarSesionView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('check/', CheckAuthView.as_view(), name='check-auth'),
    path('sesiones/', SesionesActivasView.as_view(), name='sesiones-activas'),
    path('sesiones/<int:sesion_id>/cerrar/', CerrarSesionView.as_view(), name='cerrar-sesion'),
]
