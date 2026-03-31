from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rankings', views.RankingViewSet, basename='ranking')

urlpatterns = [
    path('', include(router.urls)),
    # Ranking completo de una liga con posiciones
    path('liga/', views.ranking_por_liga, name='ranking-por-liga'),
    # Posición detallada de un usuario específico
    path('usuario/', views.posicion_usuario, name='posicion-usuario'),
    # Actualizar ranking de un usuario
    path('actualizar/', views.actualizar_ranking, name='actualizar-ranking'),
    # Recalcular ranking de toda una liga
    path('recalcular/', views.recalcular_ranking_liga, name='recalcular-ranking-liga'),
    # Mi ranking (usuario autenticado)
    path('mi-ranking/', views.mi_ranking, name='mi-ranking'),
]
