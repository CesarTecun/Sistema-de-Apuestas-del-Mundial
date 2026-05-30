from django.conf import settings
from django.core.mail import send_mail


def enviar_correo_recuperacion(usuario, token_plano):
    """Envía el correo con el enlace de recuperación de contraseña."""
    nombre = usuario.get_full_name() or usuario.email
    reset_link = f"https://frontend-pdp7.onrender.com/recuperar-contrasena?token={token_plano}"

    asunto = "Recupera tu contraseña - Sistema de Apuestas"
    mensaje = f"""
Hola {nombre},

Recibimos una solicitud para restablecer la contraseña de tu cuenta.

Para continuar, haz clic en el siguiente enlace (válido por 24 horas):
{reset_link}

Si tú no solicitaste este cambio, ignora este mensaje. Tu contraseña seguirá siendo la misma.

---
Sistema de Apuestas del Mundial 2026
Este es un correo automático, por favor no respondas a este mensaje.
"""

    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[usuario.email],
        fail_silently=True,
    )


