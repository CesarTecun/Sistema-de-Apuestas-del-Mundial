from django.contrib import admin
from .models import Liga

@admin.register(Liga)
class LigaAdmin(admin.ModelAdmin):
    list_display = ('id_liga', 'nombre_liga', 'fk_administrador', 'monto_total_recaudado', 'estado', 'tipo_liga')
    list_filter = ('estado', 'tipo_liga')
    search_fields = ('nombre_liga',)
    readonly_fields = ('id_liga',)
    ordering = ('id_liga',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_liga', 'fk_administrador')
        }),
        ('Detalles de la Liga', {
            'fields': ('monto_total_recaudado', 'estado', 'tipo_liga')
        }),
    )
