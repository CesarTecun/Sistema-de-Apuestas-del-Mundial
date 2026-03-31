from django.contrib import admin
from .models import Premio


@admin.register(Premio)
class PremioAdmin(admin.ModelAdmin):
    list_display = ('id_premio', 'fk_id_liga', 'posicion', 'porcentaje_premio')
    list_filter = ('fk_id_liga',)
    search_fields = ('fk_id_liga', 'posicion')
    ordering = ('fk_id_liga', 'posicion')
