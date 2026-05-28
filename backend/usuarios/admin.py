import secrets
from datetime import timedelta

from django import forms
from django.contrib import admin, messages
from django.utils import timezone

from backend.autenticacion.models import PasswordResetToken
from backend.autenticacion.emails import enviar_correo_recuperacion

from .models import Usuario, RolUsuario


class UsuarioAdminForm(forms.ModelForm):
    """Formulario con campo contrasena editable"""
    
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'contrasena': forms.PasswordInput,
        }

    def clean_contrasena(self):
        """Hashear contraseña si es texto plano"""
        contrasena = self.cleaned_data.get('contrasena')
        if contrasena and not contrasena.startswith('pbkdf2'):
            # Es texto plano, hashear
            from django.contrib.auth.hashers import make_password
            return make_password(contrasena)
        return contrasena


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm
    list_display = ['id_usuario', 'email', 'primer_nombre', 'primer_apellido', 'telefono', 'fk_rol']
    list_filter = ['fk_rol']
    search_fields = ['email', 'primer_nombre', 'primer_apellido']
    actions = ['enviar_enlace_recuperacion']

    @admin.action(description='Enviar enlace de restablecimiento a los usuarios seleccionados')
    def enviar_enlace_recuperacion(self, request, queryset):
        enviados = 0
        for usuario in queryset:
            if not usuario.email:
                continue

            token_obj = PasswordResetToken.objects.create(
                usuario=usuario,
                token=secrets.token_hex(32),
                expires_at=timezone.now() + timedelta(hours=24),
            )
            enviar_correo_recuperacion(token_obj)
            enviados += 1

        if enviados:
            self.message_user(
                request,
                f'Se enviaron {enviados} enlaces de restablecimiento.',
                messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                'No se enviaron enlaces. Verifique que los usuarios seleccionados tengan correo.',
                messages.WARNING,
            )


@admin.register(RolUsuario)
class RolUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_rol', 'descripcion']
