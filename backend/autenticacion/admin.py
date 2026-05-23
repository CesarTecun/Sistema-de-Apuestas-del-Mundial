from django.contrib import admin, messages

from .models import PasswordResetToken
from .emails import enviar_correo_recuperacion


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'token',
        'created_at',
        'expires_at',
        'used_at',
        'is_active',
    )
    list_filter = ('created_at', 'expires_at', 'used_at')
    search_fields = ('token', 'usuario__email')
    readonly_fields = ('token', 'created_at', 'used_at')
    actions = ('reenviar_correo_recuperacion',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and obj.is_active:
            try:
                enviar_correo_recuperacion(obj)
                self.message_user(
                    request,
                    'Se envió el correo de recuperación al crear el token.',
                    messages.SUCCESS,
                )
            except Exception as exc:
                self.message_user(
                    request,
                    f'No se pudo enviar el correo: {exc}',
                    messages.ERROR,
                )

    @admin.action(description='Reenviar correo de recuperación para los tokens seleccionados')
    def reenviar_correo_recuperacion(self, request, queryset):
        enviados = 0
        for token in queryset:
            if token.is_active:
                enviar_correo_recuperacion(token)
                enviados += 1

        if enviados:
            self.message_user(
                request,
                f'Se reenviaron {enviados} correos de recuperación.',
                messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                'No se reenviaron correos porque los tokens seleccionados están vencidos o usados.',
                messages.WARNING,
            )