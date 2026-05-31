from django.conf import settings
from django.core.mail import send_mail


INVITACION_SUBJECT = 'Invitación a una liga de la Copa Mundial FIFA 2026'


def render_mensaje_invitacion(invitacion):
    mensaje_admin = invitacion.mensaje_invitacion or 'Sin mensaje personalizado'
    login_url = "https://frontend-pdp7.onrender.com/login"
    return f"""
¡Hola!

Has sido invitado a unirte a una liga en nuestro sistema de pronósticos para la Copa Mundial FIFA 2026.

Detalles de la invitación:
• Código de invitación: {invitacion.codigo_invitacion}

Mensaje del administrador:
{mensaje_admin}

Pasos para unirte:
1. pega este enlace en tu navegador: {login_url}
2. Si no tienes cuenta todavía, créala desde esa pantalla.
3. Dentro del módulo "Ligas" presiona el botón "Unirme" y escribe tu código de invitación.

Recuerda: el código es personal y se debe ingresar respetando guiones y mayúsculas/minúsculas.

¡Que gane el mejor!

---
Copa Mundial FIFA 2026 - Sistema de Pronósticos
Este es un correo automático, por favor no respondas a este mensaje.
"""


def enviar_correo_invitacion(invitacion):
    if not invitacion.email_invitado:
        raise ValueError('La invitación no tiene correo para enviar')

    send_mail(
        subject=INVITACION_SUBJECT,
        message=render_mensaje_invitacion(invitacion),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[invitacion.email_invitado],
        fail_silently=True,
    )
