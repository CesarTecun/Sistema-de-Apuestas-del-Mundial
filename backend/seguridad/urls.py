from django.urls import path
from . import views

urlpatterns = [
    path('escanear/inyeccion/', views.escanear_inyeccion, name='seguridad-escanear-inyeccion'),
    path('auditar/autenticacion/', views.auditar_autenticacion, name='seguridad-auditar-autenticacion'),
    path('auditar/exposicion-datos/', views.auditar_exposicion_datos, name='seguridad-auditar-exposicion-datos'),
    path('escanear/xxe/', views.escanear_xxe, name='seguridad-escanear-xxe'),
    path('escanear/acceso/', views.escanear_acceso, name='seguridad-escanear-acceso'),
    path('verificar/configuracion/', views.verificar_configuracion, name='seguridad-verificar-configuracion'),
    path('probar/xss/', views.probar_xss, name='seguridad-probar-xss'),
    path('auditar/deserializacion/', views.auditar_deserializacion, name='seguridad-auditar-deserializacion'),
    path('escanear/componentes/', views.escanear_componentes, name='seguridad-escanear-componentes'),
    path('verificar/monitoreo/', views.verificar_monitoreo, name='seguridad-verificar-monitoreo'),
]
