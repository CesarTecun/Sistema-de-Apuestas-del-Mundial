from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LigaViewSet, ligas_por_usuario

router = DefaultRouter()
router.register(r'', LigaViewSet, basename='liga')  # Cambiado de 'ligas' a ''

urlpatterns = [
    path('', include(router.urls)),  # Cambiado de 'api/' a ''
    path('por-usuario/', ligas_por_usuario, name='ligas_por_usuario'),
]
