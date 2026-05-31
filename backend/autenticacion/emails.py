from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import escape


def enviar_correo_recuperacion(usuario, token_plano):
    """Envía el correo con el enlace de recuperación de contraseña."""
    nombre = usuario.get_full_name() or usuario.email
    reset_link = f"https://frontend-pdp7.onrender.com/recuperar-contrasena?token={token_plano}"

    asunto = "Recupera tu contraseña - Sistema de Apuestas"
    
    # Mensaje de texto plano (respaldo para clientes que no soportan HTML)
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

    # Versión HTML del correo
    mensaje_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .container {{
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2c3e50;
            margin: 0;
        }}
        .content {{
            margin-bottom: 30px;
        }}
        .button {{
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            margin: 20px 0;
            cursor: pointer;
        }}
        .button:hover {{
            background-color: #2980b9;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #777;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Recupera tu contraseña</h1>
        </div>
        <div class="content">
            <p>Hola <strong>{escape(nombre)}</strong>,</p>
            <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta.</p>
            <p>Para continuar, haz clic en el siguiente enlace (válido por 24 horas):</p>
            <p style="text-align: center;">
                <a href="{escape(reset_link)}" class="button">Restablecer Contraseña</a>
            </p>
            <p style="font-size: 12px; color: #666;">
                Si el botón no funciona, copia y pega este enlace en tu navegador:<br>
                <a href="{escape(reset_link)}" style="color: #3498db;">{escape(reset_link)}</a>
            </p>
            <p>Si tú no solicitaste este cambio, ignora este mensaje. Tu contraseña seguirá siendo la misma.</p>
        </div>
        <div class="footer">
            <p>Sistema de Apuestas del Mundial 2026</p>
            <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
        </div>
    </div>
</body>
</html>
"""

    send_mail(
        subject=asunto,
        message=mensaje,
        html_message=mensaje_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[usuario.email],
        fail_silently=True,
    )


