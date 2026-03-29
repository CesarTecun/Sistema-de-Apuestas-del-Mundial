"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def api_root(request):
    return Response({
        'message': 'Sistema de Apuestas del Mundial 2026 - API',
        'endpoints': {
            'admin': '/admin/',
            'auth': '/api/auth/',
            'docs': '/api/docs/',
        }
    })

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def home_view(request):
    return Response({
        'message': 'Bienvenido al Sistema de Apuestas del Mundial 2026',
        'project': 'Backend Django + Frontend React',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'auth_login': '/api/auth/login/',
            'auth_logout': '/api/auth/logout/',
        }
    })

urlpatterns = [
    path("", home_view),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", api_root),
    path("api/auth/", include("backend.autenticacion.urls")),
    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
