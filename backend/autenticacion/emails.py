from django.conf import settings
from django.core.mail import send_mail


def enviar_correo_recuperacion(usuario, token_plano):
    """Envía el correo con el enlace de recuperación de contraseña."""
    nombre = usuario.get_full_name() or usuario.email
    reset_link = f"https://frontend-pdp7.onrender.com/recuperar-contrasena?token={token_plano}"

    asunto = "Recupera tu contraseña - Sistema de Apuestas"
    mensaje_plano = f"""
Hola {nombre},

Recibimos una solicitud para restablecer la contraseña de tu cuenta.

Para continuar, haz clic en el siguiente enlace (válido por 24 horas):
{reset_link}

Si tú no solicitaste este cambio, ignora este mensaje. Tu contraseña seguirá siendo la misma.

---
Sistema de Apuestas del Mundial 2026
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
    </style>
</head>
<body>
    <div class="container">
        <h2>Recupera tu contraseña</h2>
        <p>Hola <strong>{nombre}</strong>,</p>
        <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta.</p>
        <p>Para continuar, haz clic en el siguiente botón (válido por 24 horas):</p>
        <p style="text-align: center;">
            <a href="{reset_link}" class="button">Restablecer Contraseña</a>
        </p>
        <p>O copia y pega este enlace en tu navegador:</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
        <p>Si tú no solicitaste este cambio, ignora este mensaje. Tu contraseña seguirá siendo la misma.</p>
        <hr>
        <p><small>Sistema de Apuestas del Mundial 2026<br>Este es un correo automático, por favor no respondas a este mensaje.</small></p>
    </div>
</body>
</html>
"""

    send_mail(
        subject=asunto,
        message=mensaje_plano,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[usuario.email],
        html_message=mensaje_html,
        fail_silently=True,
    )


