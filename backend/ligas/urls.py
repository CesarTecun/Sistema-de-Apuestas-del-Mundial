from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LigaViewSet, ligas_por_usuario

router = DefaultRouter()
router.register(r'ligas', LigaViewSet, basename='liga')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/ligas/por-usuario/', ligas_por_usuario, name='ligas_por_usuario'),
]
