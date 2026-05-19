from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SedeViewSet, FaseGrupoViewSet

router = DefaultRouter()
router.register(r'sedes', SedeViewSet, basename='sede')
router.register(r'fases', FaseGrupoViewSet, basename='fase')

urlpatterns = [
    path('', include(router.urls)),
]
