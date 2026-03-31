from django.contrib import admin
from .models import HistorialGanador


@admin.register(HistorialGanador)
class HistorialGanadorAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'fk_id_usuario', 'fk_id_liga', 'monto_pagado', 'fecha_premio')
    list_filter = ('fk_id_liga', 'fecha_premio')
    search_fields = ('fk_id_usuario', 'fk_id_liga')
    ordering = ('-fecha_premio',)
    readonly_fields = ('id_pago', 'fecha_premio')
