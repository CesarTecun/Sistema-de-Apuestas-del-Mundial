from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LigaViewSet,
    InvitacionViewSet,
    ParticipanteLigaViewSet,
    SolicitudParticipacionViewSet,
    LigasPublicasView,
    InvitacionPublicaView,
    ligas_por_usuario,
    enviar_invitacion_email_api,
    participantes_por_liga,
)

router = DefaultRouter()
router.register(r'invitaciones', InvitacionViewSet, basename='invitacion')
router.register(r'participantes', ParticipanteLigaViewSet, basename='participante')
router.register(r'solicitudes', SolicitudParticipacionViewSet, basename='solicitud-participacion')
router.register(r'', LigaViewSet, basename='liga')

urlpatterns = [
    path('publicas/', LigasPublicasView.as_view(), name='ligas_publicas'),
    path('por-usuario/', ligas_por_usuario, name='ligas_por_usuario'),
    path('participantes/por-liga/', participantes_por_liga, name='participantes_por_liga'),
    path('invitaciones/enviar-email/', enviar_invitacion_email_api, name='enviar_invitacion_email'),
    path('invitaciones/publico/<uuid:codigo>/', InvitacionPublicaView.as_view(), name='invitacion_publica'),
    path('', include(router.urls)),
]
