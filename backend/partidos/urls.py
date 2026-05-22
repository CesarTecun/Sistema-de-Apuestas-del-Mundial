from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PartidoViewSet, JugadorViewSet, SeleccionViewSet,
    partidos_por_liga, partidos_por_equipo, actualizar_resultado,
    bracket_eliminatoria, generar_bracket
)
from . import marcador_views

router = DefaultRouter()
router.register(r'partidos', PartidoViewSet, basename='partido')
router.register(r'jugadores', JugadorViewSet, basename='jugador')
router.register(r'selecciones', SeleccionViewSet, basename='seleccion')

urlpatterns = [
    path('', include(router.urls)),
    path('por-liga/', partidos_por_liga, name='partidos_por_liga'),
    path('por-equipo/', partidos_por_equipo, name='partidos_por_equipo'),
    path('<int:pk>/actualizar-resultado/', actualizar_resultado, name='actualizar_resultado'),
    path('marcador/webhook/', marcador_views.marcador_webhook, name='marcador_webhook'),
    path('bracket/', bracket_eliminatoria, name='bracket_eliminatoria'),
    path('bracket/generar/', generar_bracket, name='generar_bracket'),
    # --- Proxy al microservicio Marcador ---
    path('marcador/selecciones/', marcador_views.marcador_selecciones, name='marcador_selecciones'),
    path('marcador/partidos/', marcador_views.marcador_partidos, name='marcador_partidos'),
    path('marcador/partidos/todos/', marcador_views.marcador_partidos_en_vivo, name='marcador_partidos_todos'),
    path('marcador/partidos/en-vivo/', marcador_views.marcador_partidos_en_vivo, name='marcador_partidos_en_vivo'),
    path('marcador/partidos/<int:id_partido>/', marcador_views.marcador_partido_detalle, name='marcador_partido_detalle'),
    path('marcador/partidos/por-equipo/', marcador_views.marcador_partidos_por_equipo, name='marcador_partidos_por_equipo'),
    path('marcador/partidos/crear/', marcador_views.marcador_crear_partido, name='marcador_crear_partido'),
    path('marcador/partidos/<int:id_partido>/actualizar/', marcador_views.marcador_actualizar_partido, name='marcador_actualizar_partido'),
    path('marcador/partidos/<int:id_partido>/actualizar-marcador/', marcador_views.marcador_actualizar_marcador, name='marcador_actualizar_marcador'),
    path('marcador/partidos/<int:id_partido>/eliminar/', marcador_views.marcador_eliminar_partido, name='marcador_eliminar_partido'),
    path('marcador/partidos/<int:id_partido>/control/', marcador_views.marcador_controlar_partido, name='marcador_controlar_partido'),
    path('marcador/health/', marcador_views.marcador_health, name='marcador_health'),
]
