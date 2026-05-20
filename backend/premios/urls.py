from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'premios', views.PremioViewSet, basename='premio')

urlpatterns = [
    path('', include(router.urls)),
    # Obtener premios calculados de una liga (basado en ranking)
    path('liga/', views.premios_liga, name='premios-liga'),
    # Obtener mi premio en una liga
    path('mi-premio/', views.mi_premio, name='mi-premio'),
    # Obtener distribución configurada de una liga
    path('distribucion/', views.distribucion_liga, name='distribucion-liga'),
    # Configurar distribución de premios (admin)
    path('configurar/', views.configurar_premios, name='configurar-premios'),
    # Inicializar premios con distribución por defecto (admin)
    path('inicializar/', views.inicializar_premios_default, name='inicializar-premios'),
    # Obtener premio de un usuario específico
    path('usuario/', views.premio_usuario_liga, name='premio-usuario-liga'),
    # Cerrar liga y distribuir premios (admin)
    path('cerrar/', views.ejecutar_cierre_liga, name='cerrar-liga'),
    # Simular cierre de liga sin persistir
    path('simular/', views.simular_cierre_liga, name='simular-cierre-liga'),
    # Premios globales de todas las ligas
    path('globales/', views.premios_globales, name='premios-globales'),
]
