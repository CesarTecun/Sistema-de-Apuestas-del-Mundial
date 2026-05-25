from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SedeViewSet, FaseGrupoViewSet,
    BitacoraViewSet, AuditLogViewSet,
    ConfiguracionTorneoView, reporte_resumen,
)

router = DefaultRouter()
router.register(r'sedes', SedeViewSet, basename='sede')
router.register(r'fases', FaseGrupoViewSet, basename='fase')
router.register(r'bitacora', BitacoraViewSet, basename='bitacora')
router.register(r'audit-log', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
    path('configuracion/', ConfiguracionTorneoView.as_view(), name='configuracion-torneo'),
    path('reportes/resumen/', reporte_resumen, name='reporte-resumen'),
]
