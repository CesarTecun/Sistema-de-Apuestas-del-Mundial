from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartidoViewSet, partidos_por_liga, partidos_por_equipo, actualizar_resultado

router = DefaultRouter()
router.register(r'partidos', PartidoViewSet, basename='partido')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/partidos/por-liga/', partidos_por_liga, name='partidos_por_liga'),
    path('api/partidos/por-equipo/', partidos_por_equipo, name='partidos_por_equipo'),
    path('api/partidos/<int:pk>/actualizar-resultado/', actualizar_resultado, name='actualizar_resultado'),
]
