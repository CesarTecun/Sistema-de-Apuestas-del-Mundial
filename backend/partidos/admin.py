from django.contrib import admin
from .models import Partido, Jugador, Seleccion


@admin.register(Seleccion)
class SeleccionAdmin(admin.ModelAdmin):
    list_display = ('id_seleccion', 'pais', 'codigo_iso')
    search_fields = ('pais',)


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('id_jugador', 'primer_nombre', 'dorsal', 'posicion', 'fk_id_seleccion')
    search_fields = ('primer_nombre', 'dorsal')
    list_filter = ('posicion',)


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('id_partido', 'horario', 'equipo_local', 'equipo_visitante', 'gol_local', 'gol_visitante', 'resultado', 'tipo_partido')
    list_filter = ('tipo_partido', 'fk_id_fase')
    search_fields = ('equipo_local', 'equipo_visitante', 'resultado')
    readonly_fields = ('id_partido',)
    ordering = ('-horario', 'id_partido')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('equipo_local', 'equipo_visitante', 'fk_sede', 'fk_id_fase')
        }),
        ('Fecha y Tipo', {
            'fields': ('horario', 'tipo_partido')
        }),
        ('Resultado del Partido', {
            'fields': ('gol_local', 'gol_visitante', 'ganador_penales', 'resultado')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Hacer readonly algunos campos después de crear"""
        if obj and obj.pk:
            return self.readonly_fields + ('equipo_local', 'equipo_visitante', 'fk_sede', 'fk_id_fase')
        return self.readonly_fields
