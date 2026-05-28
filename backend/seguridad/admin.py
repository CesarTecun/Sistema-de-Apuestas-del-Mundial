from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render
from django.utils.html import format_html

from .models import (
    VulnerabilidadInyeccion,
    FallaAutenticacion,
    ExposicionDatos,
    VulnerabilidadXXE,
    AuditoriaAcceso,
    ConfiguracionSeguridad,
    VulnerabilidadXSS,
    IntentoDeserializacion,
    ComponenteVulnerable,
    RegistroMonitoreo,
    PanelOWASP,
)


@admin.register(VulnerabilidadInyeccion)
class VulnerabilidadInyeccionAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'metodo', 'parametro', 'tipo_inyeccion', 'resultado', 'fecha_escaneo')
    list_filter = ('tipo_inyeccion', 'resultado', 'fecha_escaneo')
    search_fields = ('endpoint', 'parametro', 'payload')
    readonly_fields = ('fecha_escaneo',)


@admin.register(FallaAutenticacion)
class FallaAutenticacionAdmin(admin.ModelAdmin):
    list_display = ('modulo', 'problema', 'severidad', 'estado', 'fecha_deteccion')
    list_filter = ('severidad', 'estado', 'fecha_deteccion')
    search_fields = ('modulo', 'problema', 'recomendacion')
    readonly_fields = ('fecha_deteccion',)
    actions = ('marcar_mitigado',)

    @admin.action(description='Marcar como mitigado')
    def marcar_mitigado(self, request, queryset):
        queryset.update(estado='Mitigado')


@admin.register(ExposicionDatos)
class ExposicionDatosAdmin(admin.ModelAdmin):
    list_display = ('origen', 'tipo_dato', 'riesgo', 'fecha_deteccion')
    list_filter = ('riesgo', 'fecha_deteccion')
    search_fields = ('origen', 'tipo_dato', 'exposicion')
    readonly_fields = ('fecha_deteccion',)


@admin.register(VulnerabilidadXXE)
class VulnerabilidadXXEAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'parser', 'permite_dtd', 'permite_entities', 'resultado', 'fecha_escaneo')
    list_filter = ('resultado', 'permite_dtd', 'permite_entities', 'fecha_escaneo')
    search_fields = ('endpoint', 'parser')
    readonly_fields = ('fecha_escaneo',)


@admin.register(AuditoriaAcceso)
class AuditoriaAccesoAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'metodo', 'requiere_auth', 'auth_configurado', 'riesgo', 'fecha_escaneo')
    list_filter = ('riesgo', 'requiere_auth', 'auth_configurado', 'fecha_escaneo')
    search_fields = ('endpoint', 'observacion')
    readonly_fields = ('fecha_escaneo',)
    actions = ('marcar_como_revisado',)

    @admin.action(description='Marcar como riesgo medio')
    def marcar_como_revisado(self, request, queryset):
        queryset.update(riesgo='Medio')


@admin.register(ConfiguracionSeguridad)
class ConfiguracionSeguridadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'valor_actual', 'valor_recomendado', 'fecha_verificacion')
    list_filter = ('estado', 'fecha_verificacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_verificacion',)


@admin.register(VulnerabilidadXSS)
class VulnerabilidadXSSAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'vector_corto', 'resultado', 'fecha_prueba')
    list_filter = ('resultado', 'fecha_prueba')
    search_fields = ('endpoint', 'vector')
    readonly_fields = ('fecha_prueba',)

    def vector_corto(self, obj):
        return obj.vector[:60] + '...' if len(obj.vector) > 60 else obj.vector
    vector_corto.short_description = 'Vector'


@admin.register(IntentoDeserializacion)
class IntentoDeserializacionAdmin(admin.ModelAdmin):
    list_display = ('origen', 'tipo_dato', 'permitido', 'riesgo', 'fecha_deteccion')
    list_filter = ('tipo_dato', 'permitido', 'riesgo', 'fecha_deteccion')
    search_fields = ('origen', 'recomendacion')
    readonly_fields = ('fecha_deteccion',)


@admin.register(ComponenteVulnerable)
class ComponenteVulnerableAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'version', 'cve_id', 'severidad', 'estado', 'fecha_deteccion')
    list_filter = ('severidad', 'estado', 'fecha_deteccion')
    search_fields = ('nombre', 'cve_id', 'descripcion')
    readonly_fields = ('fecha_deteccion',)
    actions = ('marcar_mitigado',)

    @admin.action(description='Marcar como mitigado')
    def marcar_mitigado(self, request, queryset):
        queryset.update(estado='Mitigado')


@admin.register(RegistroMonitoreo)
class RegistroMonitoreoAdmin(admin.ModelAdmin):
    list_display = ('evento', 'nivel', 'usuario', 'ip_address', 'fecha_evento')
    list_filter = ('nivel', 'fecha_evento')
    search_fields = ('evento', 'detalle', 'usuario')
    readonly_fields = ('fecha_evento',)
    date_hierarchy = 'fecha_evento'


@admin.register(PanelOWASP)
class PanelOWASPAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ultima_actualizacion', 'ir_al_panel')
    readonly_fields = ('ultima_actualizacion',)

    def ir_al_panel(self, obj):
        return format_html(
            '<a class="button" style="padding:6px 12px;background:#417690;color:#fff;text-decoration:none;border-radius:4px;" href="{}">Abrir Panel OWASP</a>',
            reverse('admin:seguridad-panel')
        )
    ir_al_panel.short_description = 'Panel'
    ir_al_panel.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('panel/', self.admin_site.admin_view(self.panel_view), name='seguridad-panel'),
        ]
        return custom_urls + urls

    def panel_view(self, request):
        context = {
            'title': 'Panel OWASP - Top 10',
            'opts': self.model._meta,
            'has_permission': self.has_view_permission(request),
            'api_endpoints': [
                {'codigo': 'A01', 'nombre': 'Inyeccion', 'url': '/api/seguridad/escanear/inyeccion/'},
                {'codigo': 'A02', 'nombre': 'Autenticacion interrumpida', 'url': '/api/seguridad/auditar/autenticacion/'},
                {'codigo': 'A03', 'nombre': 'Exposicion de datos confidenciales', 'url': '/api/seguridad/auditar/exposicion-datos/'},
                {'codigo': 'A04', 'nombre': 'Entidades externas XML (XXE)', 'url': '/api/seguridad/escanear/xxe/'},
                {'codigo': 'A05', 'nombre': 'Control de Acceso Roto', 'url': '/api/seguridad/escanear/acceso/'},
                {'codigo': 'A06', 'nombre': 'Configuraciones Incorrectas', 'url': '/api/seguridad/verificar/configuracion/'},
                {'codigo': 'A07', 'nombre': 'XSS', 'url': '/api/seguridad/probar/xss/'},
                {'codigo': 'A08', 'nombre': 'Desserializacion Insegura', 'url': '/api/seguridad/auditar/deserializacion/'},
                {'codigo': 'A09', 'nombre': 'Componentes Vulnerables', 'url': '/api/seguridad/escanear/componentes/'},
                {'codigo': 'A10', 'nombre': 'Registro y Monitoreo', 'url': '/api/seguridad/verificar/monitoreo/'},
            ],
            **self.admin_site.each_context(request),
        }
        return render(request, 'admin/seguridad/panel.html', context)
