from django.contrib import admin
from .models import Pronostico

@admin.register(Pronostico)
class PronosticoAdmin(admin.ModelAdmin):
    list_display = ('id_pronostico', 'fk_id_usuario', 'fk_id_partido', 'fk_id_liga', 'gol_local', 'gol_visitante', 'ganador_pronostico')
    list_filter = ('fk_id_liga', 'fk_id_usuario')
    search_fields = ('fk_id_usuario', 'fk_id_partido', 'fk_id_liga')
    readonly_fields = ('id_pronostico',)
    ordering = ('-id_pronostico',)
    
    fieldsets = (
        ('Información del Pronóstico', {
            'fields': ('fk_id_usuario', 'fk_id_partido', 'fk_id_liga')
        }),
        ('Resultado Pronosticado', {
            'fields': ('gol_local', 'gol_visitante')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Hacer readonly algunos campos después de crear"""
        if obj and obj.pk:
            return self.readonly_fields + ('fk_id_usuario', 'fk_id_partido', 'fk_id_liga')
        return self.readonly_fields
    
    def ganador_pronostico(self, obj):
        """Mostrar el ganador según el pronóstico"""
        if obj.gol_local > obj.gol_visitante:
            return 'Local'
        elif obj.gol_visitante > obj.gol_local:
            return 'Visitante'
        else:
            return 'Empate'
    ganador_pronostico.short_description = 'Ganador Pronosticado'
