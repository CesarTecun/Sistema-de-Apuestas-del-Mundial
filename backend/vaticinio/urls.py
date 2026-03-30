from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PronosticoViewSet, 
    pronosticos_por_usuario, 
    pronosticos_por_liga, 
    pronosticos_por_partido,
    pronosticos_usuario_liga,
    verificar_pronostico_disponible
)

router = DefaultRouter()
router.register(r'pronosticos', PronosticoViewSet, basename='pronostico')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/pronosticos/por-usuario/', pronosticos_por_usuario, name='pronosticos_por_usuario'),
    path('api/pronosticos/por-liga/', pronosticos_por_liga, name='pronosticos_por_liga'),
    path('api/pronosticos/por-partido/', pronosticos_por_partido, name='pronosticos_por_partido'),
    path('api/pronosticos/usuario-liga/', pronosticos_usuario_liga, name='pronosticos_usuario_liga'),
    path('api/pronosticos/verificar-disponible/', verificar_pronostico_disponible, name='verificar_pronostico_disponible'),
]
