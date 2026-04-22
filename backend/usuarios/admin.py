from django.contrib import admin
from django import forms
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


@admin.register(RolUsuario)
class RolUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_rol', 'descripcion']
