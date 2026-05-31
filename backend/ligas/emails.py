from django.conf import settings
from django.core.mail import send_mail


INVITACION_SUBJECT = 'Invitación a una liga de la Copa Mundial FIFA 2026'


def render_mensaje_invitacion(invitacion):
    mensaje_admin = invitacion.mensaje_invitacion or 'Sin mensaje personalizado'
    login_url = "https://frontend-pdp7.onrender.com/login"

    mensaje_plano = f"""
¡Hola!

Has sido invitado a unirte a una liga en nuestro sistema de pronósticos para la Copa Mundial FIFA 2026.

Detalles de la invitación:
• Código de invitación: {invitacion.codigo_invitacion}

Mensaje del administrador:
{mensaje_admin}

Pasos para unirte:
1. Haz clic en el siguiente enlace: {login_url}
2. Si no tienes cuenta todavía, créala desde esa pantalla.
3. Dentro del módulo "Ligas" presiona el botón "Unirme" y escribe tu código de invitación.

Recuerda: el código es personal y se debe ingresar respetando guiones y mayúsculas/minúsculas.

¡Que gane el mejor!

---
Copa Mundial FIFA 2026 - Sistema de Pronósticos
Este es un correo automático, por favor no respondas a este mensaje.
"""

    mensaje_html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .button {{ display: inline-block; padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; }}
        .button:hover {{ background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); }}
        .code {{ background: #f5f5f5; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 16px; letter-spacing: 2px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>¡Invitación a una Liga!</h2>
        <p>¡Hola!</p>
        <p>Has sido invitado a unirte a una liga en nuestro sistema de pronósticos para la Copa Mundial FIFA 2026.</p>

        <h3>Detalles de la invitación:</h3>
        <p><strong>Código de invitación:</strong> <span class="code">{invitacion.codigo_invitacion}</span></p>

        <h3>Mensaje del administrador:</h3>
        <p>{mensaje_admin}</p>

        <h3>Pasos para unirte:</h3>
        <ol>
            <li>Haz clic en el siguiente botón para ir al sistema:</li>
        </ol>
        <p style="text-align: center;">
            <a href="{login_url}" class="button">Ir al Sistema</a>
        </p>
        <ol start="2">
            <li>Si no tienes cuenta todavía, créala desde esa pantalla.</li>
            <li>Dentro del módulo "Ligas" presiona el botón "Unirme" y escribe tu código de invitación.</li>
        </ol>

        <p><em>Recuerda: el código es personal y se debe ingresar respetando guiones y mayúsculas/minúsculas.</em></p>

        <p>¡Que gane el mejor!</p>

        <hr>
        <p><small>Copa Mundial FIFA 2026 - Sistema de Pronósticos<br>Este es un correo automático, por favor no respondas a este mensaje.</small></p>
    </div>
</body>
</html>
"""

    return mensaje_plano, mensaje_html


def enviar_correo_invitacion(invitacion):
    if not invitacion.email_invitado:
        raise ValueError('La invitación no tiene correo para enviar')

    mensaje_plano, mensaje_html = render_mensaje_invitacion(invitacion)

    send_mail(
        subject=INVITACION_SUBJECT,
        message=mensaje_plano,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[invitacion.email_invitado],
        html_message=mensaje_html,
        fail_silently=True,
    )
