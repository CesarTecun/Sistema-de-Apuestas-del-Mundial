from django.conf import settings
from django.core.mail import send_mail


INVITACION_SUBJECT = '🏆 Has sido invitado a una Liga de la Copa Mundial FIFA 2026'


def render_mensaje_invitacion(invitacion):
    mensaje_admin = invitacion.mensaje_invitacion or 'Sin mensaje personalizado'
    enlace = f"{settings.FRONTEND_URL}/invitaciones/{invitacion.id_invitacion}"
    return f"""
¡Hola!

Has sido invitado a unirte a una liga en nuestro sistema de pronósticos para la Copa Mundial FIFA 2026.

📋 Detalles de la invitación:
• ID de Liga: {invitacion.fk_id_liga}
• Estado: {invitacion.estado_invitacion}

💬 Mensaje del administrador:
{mensaje_admin}

🔗 Para aceptar la invitación ingresa a: {enlace}

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
        fail_silently=False,
    )
