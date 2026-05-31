from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PronosticoViewSet,
    pronosticos_por_usuario,
    pronosticos_por_liga,
    pronosticos_por_partido,
    pronosticos_por_partido_liga,
    pronosticos_usuario_liga,
    verificar_pronostico_disponible,
    historial_usuario
)

router = DefaultRouter()
router.register(r'pronosticos', PronosticoViewSet, basename='pronostico')

urlpatterns = [
    # Rutas personalizadas DEBEN ir antes del router para no colisionar con {pk}/
    path('por-usuario/', pronosticos_por_usuario, name='pronosticos_por_usuario'),
    path('por-liga/', pronosticos_por_liga, name='pronosticos_por_liga'),
    path('por-partido/', pronosticos_por_partido, name='pronosticos_por_partido'),
    path('por-partido-liga/', pronosticos_por_partido_liga, name='pronosticos_por_partido_liga'),
    path('usuario-liga/', pronosticos_usuario_liga, name='pronosticos_usuario_liga'),
    path('verificar-disponible/', verificar_pronostico_disponible, name='verificar_pronostico_disponible'),
    path('mi-historial/', historial_usuario, name='historial_usuario'),
    # Router DRF (debe ir al final para no capturar las rutas de arriba)
    path('', include(router.urls)),
]
