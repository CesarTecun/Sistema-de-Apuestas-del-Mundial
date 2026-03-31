from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'historial', views.HistorialGanadorViewSet, basename='historial-ganador')

urlpatterns = [
    path('', include(router.urls)),
    # Historial de ganadores por liga
    path('liga/', views.historial_por_liga, name='historial-por-liga'),
    # Mis premios (usuario autenticado)
    path('mis-premios/', views.mis_premios, name='mis-premios'),
    # Resumen completo (admin)
    path('resumen/', views.resumen_historial, name='resumen-historial'),
]
