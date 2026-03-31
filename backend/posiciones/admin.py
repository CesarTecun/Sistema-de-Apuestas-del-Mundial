from django.contrib import admin
from .models import Ranking


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('id_registro', 'fk_id_usuario', 'fk_id_liga', 'puntos', 'pj', 'fecha_actualizacion')
    list_filter = ('fk_id_liga',)
    search_fields = ('fk_id_usuario', 'fk_id_liga')
    ordering = ('-puntos',)
    readonly_fields = ('id_registro', 'fecha_actualizacion')
