from django.contrib import admin, messages
from .models import Liga, Invitacion
from .emails import enviar_correo_invitacion


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


@admin.register(Invitacion)
class InvitacionAdmin(admin.ModelAdmin):
    list_display = ('id_invitacion', 'fk_id_liga', 'email_invitado', 'estado_invitacion', 'codigo_invitacion', 'fecha_invitacion')
    list_filter = ('estado_invitacion', 'fecha_invitacion')
    search_fields = ('email_invitado', 'codigo_invitacion', 'mensaje_invitacion')
    readonly_fields = ('id_invitacion', 'codigo_invitacion', 'fecha_invitacion')
    ordering = ('-fecha_invitacion',)
    
    fieldsets = (
        ('Información de la Invitación', {
            'fields': ('id_invitacion', 'codigo_invitacion', 'fk_id_liga', 'email_invitado')
        }),
        ('Participantes', {
            'fields': ('fk_id_usuario_invitado', 'fk_id_usuario_administrador')
        }),
        ('Estado y Mensaje', {
            'fields': ('estado_invitacion', 'mensaje_invitacion', 'fecha_invitacion')
        }),
    )
    
    actions = ['enviar_invitacion_email']
    
    @admin.action(description='Enviar invitación por correo')
    def enviar_invitacion_email(self, request, queryset):
        """Acción para enviar invitaciones seleccionadas por correo"""
        enviadas = 0
        errores = 0
        
        for invitacion in queryset.filter(estado_invitacion='Pendiente'):
            if invitacion.email_invitado:
                try:
                    enviar_correo_invitacion(invitacion)
                    enviadas += 1
                except Exception as e:
                    errores += 1
                    self.message_user(
                        request,
                        f"Error al enviar a {invitacion.email_invitado}: {str(e)}",
                        messages.ERROR
                    )
        
        if enviadas > 0:
            self.message_user(
                request,
                f'✅ {enviadas} invitación(es) enviada(s) exitosamente por correo.',
                messages.SUCCESS
            )
        
        if errores > 0:
            self.message_user(
                request,
                f'⚠️ {errores} invitación(es) no pudieron ser enviadas.',
                messages.WARNING
            )
        
        if enviadas == 0 and errores == 0:
            self.message_user(
                request,
                'ℹ️ No se encontraron invitaciones pendientes con email para enviar.',
                messages.INFO
            )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and obj.email_invitado and obj.estado_invitacion == 'Pendiente':
            try:
                enviar_correo_invitacion(obj)
                self.message_user(
                    request,
                    f'Correo enviado a {obj.email_invitado}',
                    messages.SUCCESS
                )
            except Exception as exc:
                self.message_user(
                    request,
                    f'No se pudo enviar correo a {obj.email_invitado}: {exc}',
                    messages.ERROR
                )
