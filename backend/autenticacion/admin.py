import hashlib
import secrets
from datetime import timedelta
from django.contrib import admin, messages
from django.utils import timezone

from .models import PasswordResetToken, EmailVerificationToken
from .emails import enviar_correo_recuperacion


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'token_hash',
        'created_at',
        'expires_at',
        'used_at',
        'is_active',
    )
    list_filter = ('created_at', 'expires_at', 'used_at')
    search_fields = ('token_hash', 'usuario__email')
    readonly_fields = ('token_hash', 'created_at', 'used_at')
    actions = ('reenviar_correo_recuperacion',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and obj.is_active:
            try:
                # Generar token plano temporal para enviar correo
                token_plano = secrets.token_hex(32)
                # Actualizar el hash en el objeto
                obj.token_hash = hashlib.sha256(token_plano.encode()).hexdigest()
                obj.save(update_fields=['token_hash'])
                enviar_correo_recuperacion(obj.usuario, token_plano)
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
                # Generar nuevo token y actualizar hash
                token_plano = secrets.token_hex(32)
                token.token_hash = hashlib.sha256(token_plano.encode()).hexdigest()
                token.expires_at = timezone.now() + timedelta(hours=24)
                token.save(update_fields=['token_hash', 'expires_at'])
                enviar_correo_recuperacion(token.usuario, token_plano)
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


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'token_hash',
        'created_at',
        'expires_at',
        'used_at',
        'is_active',
    )
    list_filter = ('created_at', 'expires_at', 'used_at')
    search_fields = ('token_hash', 'usuario__email')
    readonly_fields = ('token_hash', 'created_at', 'used_at')