from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LigaViewSet, InvitacionViewSet, ligas_por_usuario, enviar_invitacion_email_api

router = DefaultRouter()
router.register(r'', LigaViewSet, basename='liga')
router.register(r'invitaciones', InvitacionViewSet, basename='invitacion')

urlpatterns = [
    path('', include(router.urls)),
    path('por-usuario/', ligas_por_usuario, name='ligas_por_usuario'),
    path('invitaciones/enviar-email/', enviar_invitacion_email_api, name='enviar_invitacion_email'),
]
