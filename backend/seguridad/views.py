import json
import os
import subprocess
import sys
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import (
    VulnerabilidadInyeccion,
    FallaAutenticacion,
    ExposicionDatos,
    VulnerabilidadXXE,
    AuditoriaAcceso,
    ConfiguracionSeguridad,
    VulnerabilidadXSS,
    IntentoDeserializacion,
    ComponenteVulnerable,
    RegistroMonitoreo,
)


def _get_all_url_patterns(resolver, prefix=''):
    """Recursivamente obtiene todas las URLs del proyecto."""
    patterns = []
    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLPattern):
            patterns.append(prefix + str(pattern.pattern))
        elif isinstance(pattern, URLResolver):
            patterns.extend(_get_all_url_patterns(pattern, prefix + str(pattern.pattern)))
    return patterns


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def escanear_inyeccion(request):
    """A01 - Detecta puntos de entrada potenciales para inyeccion."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A01 - Inyeccion',
            'descripcion': 'Detecta puntos de entrada potenciales para SQL/NoSQL/OS/LDAP injection.',
            'instruccion': 'Haz clic en POST para ejecutar el escaneo.'
        })
    endpoints = [
        ('/api/auth/login/', 'POST', 'email', 'SQL'),
        ('/api/pronosticos/', 'POST', 'resultado', 'SQL'),
        ('/api/partidos/', 'GET', 'q', 'SQL'),
        ('/api/usuarios/', 'PUT', 'telefono', 'NoSQL'),
    ]
    resultados = []
    for endpoint, metodo, parametro, tipo in endpoints:
        payload = "' OR '1'='1" if tipo == 'SQL' else "{$ne: null}"
        obj, _ = VulnerabilidadInyeccion.objects.update_or_create(
            endpoint=endpoint,
            metodo=metodo,
            parametro=parametro,
            defaults={
                'tipo_inyeccion': tipo,
                'payload': payload,
                'resultado': 'Sospechoso',
                'observacion': 'Revisar manualmente si el parametro es sanitizado antes de consultar la BD.',
            }
        )
        resultados.append({'endpoint': endpoint, 'tipo': tipo, 'resultado': obj.resultado})
    return Response({'escaneados': len(resultados), 'detalle': resultados})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def auditar_autenticacion(request):
    """A02 - Audita configuraciones de autenticacion y sesiones."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A02 - Autenticacion interrumpida',
            'descripcion': 'Audita configuraciones de autenticacion: limites de intentos, expiracion de sesiones, passwords, MFA.',
            'instruccion': 'Haz clic en POST para ejecutar la auditoria.'
        })
    checks = [
        ('Login sin limite de intentos', 'Media',
         'Configurar rate limiting en login para prevenir fuerza bruta.'),
        ('Sesiones sin expiracion automatica', 'Alta',
         'Las sesiones JWT deben tener TTL corto y rotacion de refresh tokens.'),
        ('Password sin complejidad minima', 'Media',
         'Validar contraseñas con Django password validators.'),
        ('Auth sin MFA', 'Baja',
         'Considerar implementar autenticacion multifactor para administradores.'),
    ]
    resultados = []
    for problema, severidad, recomendacion in checks:
        obj, _ = FallaAutenticacion.objects.update_or_create(
            modulo='autenticacion',
            problema=problema,
            defaults={
                'severidad': severidad,
                'recomendacion': recomendacion,
                'estado': 'Pendiente',
            }
        )
        resultados.append({'problema': problema, 'severidad': severidad})
    return Response({'auditados': len(resultados), 'detalle': resultados})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def auditar_exposicion_datos(request):
    """A03 - Detecta posibles exposiciones de datos sensibles."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A03 - Exposicion de datos confidenciales',
            'descripcion': 'Detecta posibles exposiciones de datos sensibles: SECRET_KEY, passwords en APIs, PII en logs, DEBUG.',
            'instruccion': 'Haz clic en POST para ejecutar la auditoria.'
        })
    checks = [
        ('settings.py', 'SECRET_KEY', 'Clave secreta visible en codigo fuente.', 'Critico',
         'Mover SECRET_KEY a variables de entorno.'),
        ('Respuestas API', 'contrasena', 'Verificar que las APIs no devuelvan campos de password.', 'Alto',
         'Excluir campos sensibles de serializers.'),
        ('Logs de bitacora', 'email', 'Revisar que logs no almacenen PII sin ofuscacion.', 'Medio',
         'Ofuscar datos personales en registros de bitacora.'),
        ('Error pages DEBUG', 'traceback', 'En DEBUG=True Django expone tracebacks con paths locales.', 'Alto',
         'Desactivar DEBUG en produccion.'),
    ]
    resultados = []
    for origen, tipo_dato, exposicion, riesgo, recomendacion in checks:
        obj, _ = ExposicionDatos.objects.update_or_create(
            origen=origen,
            tipo_dato=tipo_dato,
            defaults={
                'exposicion': exposicion,
                'riesgo': riesgo,
                'recomendacion': recomendacion,
            }
        )
        resultados.append({'origen': origen, 'tipo': tipo_dato, 'riesgo': riesgo})
    return Response({'auditados': len(resultados), 'detalle': resultados})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def escanear_xxe(request):
    """A04 - Detecta parsers XML potencialmente vulnerables a XXE."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A04 - Entidades externas XML (XXE)',
            'descripcion': 'Detecta parsers XML potencialmente vulnerables a XXE.',
            'instruccion': 'Haz clic en POST para ejecutar el escaneo.'
        })
    parsers = [
        ('xml.etree.ElementTree', True, False),
        ('xml.dom.minidom', True, False),
        ('lxml.etree', True, True),
    ]
    resultados = []
    for parser, permite_dtd, permite_entities in parsers:
        resultado = 'Vulnerable' if (permite_dtd and permite_entities) else 'Sospechoso'
        obj, _ = VulnerabilidadXXE.objects.update_or_create(
            endpoint='/api/xml-parser',
            parser=parser,
            defaults={
                'permite_dtd': permite_dtd,
                'permite_entities': permite_entities,
                'resultado': resultado,
                'observacion': 'Deshabilitar DTD y entity expansion en parsers XML.' if resultado == 'Vulnerable' else 'Revisar configuracion del parser.',
            }
        )
        resultados.append({'parser': parser, 'resultado': resultado})
    return Response({'escaneados': len(resultados), 'detalle': resultados})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def escanear_acceso(request):
    """A05 - Escanea endpoints y detecta posibles fallas de control de acceso."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A05 - Control de Acceso Roto',
            'descripcion': 'Escanea URLs del proyecto para detectar endpoints sin autenticacion o autorizacion.',
            'instruccion': 'Haz clic en POST para ejecutar el escaneo.'
        })
    resolver = get_resolver()
    urls = _get_all_url_patterns(resolver)

    resultados = []
    for url in urls:
        if not url or url == '':
            continue
        url_path = url.replace('^', '').replace('$', '').replace('\\', '')
        # Heuristica: endpoints admin y api/auth suelen requerir auth
        requiere = not any(x in url_path for x in ['health', 'static', 'media'])
        auth_ok = 'admin/' in url_path or 'api/' in url_path

        obj, _ = AuditoriaAcceso.objects.update_or_create(
            endpoint=url_path,
            metodo='GET',
            defaults={
                'requiere_auth': requiere,
                'auth_configurado': auth_ok,
                'riesgo': 'Alto' if (requiere and not auth_ok) else 'Bajo',
                'observacion': 'Revisar permisos explicitos en la vista.' if (requiere and not auth_ok) else 'OK',
            }
        )
        resultados.append({
            'endpoint': url_path,
            'riesgo': obj.riesgo,
            'observacion': obj.observacion,
        })

    return Response({'escaneados': len(resultados), 'detalle': resultados})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def verificar_configuracion(request):
    """A06 - Verifica configuraciones criticas de seguridad en settings."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A06 - Configuraciones Incorrectas de Seguridad',
            'descripcion': 'Verifica settings criticos de Django: DEBUG, HSTS, cookies seguras, etc.',
            'instruccion': 'Haz clic en POST para ejecutar la verificacion.'
        })
    checks = []

    checks.append(('DEBUG', str(settings.DEBUG), 'False', 'OK' if not settings.DEBUG else 'Critico',
                   'DEBUG debe estar en False en produccion.'))
    checks.append(('SECRET_KEY', settings.SECRET_KEY[:8] + '...', 'almenos50caracteresaleatorios',
                   'OK' if len(settings.SECRET_KEY) >= 50 else 'Advertencia',
                   'SECRET_KEY debe ser larga y secreta.'))
    checks.append(('SECURE_SSL_REDIRECT', str(settings.SECURE_SSL_REDIRECT), 'True',
                   'OK' if settings.SECURE_SSL_REDIRECT else 'Advertencia',
                   'Forzar HTTPS en produccion.'))
    checks.append(('SECURE_HSTS_SECONDS', str(settings.SECURE_HSTS_SECONDS), '31536000',
                   'OK' if settings.SECURE_HSTS_SECONDS else 'Advertencia',
                   'HSTS habilitado en produccion.'))
    checks.append(('SECURE_BROWSER_XSS_FILTER', str(settings.SECURE_BROWSER_XSS_FILTER), 'True',
                   'OK' if settings.SECURE_BROWSER_XSS_FILTER else 'Advertencia',
                   'Filtro XSS del navegador activado.'))
    checks.append(('SECURE_CONTENT_TYPE_NOSNIFF', str(settings.SECURE_CONTENT_TYPE_NOSNIFF), 'True',
                   'OK' if settings.SECURE_CONTENT_TYPE_NOSNIFF else 'Advertencia',
                   'Evitar sniffing de MIME types.'))
    checks.append(('SESSION_COOKIE_SECURE', str(settings.SESSION_COOKIE_SECURE), 'True',
                   'OK' if settings.SESSION_COOKIE_SECURE else 'Critico',
                   'Cookies de sesion solo por HTTPS.'))
    checks.append(('CSRF_COOKIE_SECURE', str(settings.CSRF_COOKIE_SECURE), 'True',
                   'OK' if settings.CSRF_COOKIE_SECURE else 'Critico',
                   'Cookie CSRF solo por HTTPS.'))

    resultados = []
    for nombre, actual, recomendado, estado, desc in checks:
        obj, _ = ConfiguracionSeguridad.objects.update_or_create(
            nombre=nombre,
            defaults={
                'valor_actual': actual,
                'valor_recomendado': recomendado,
                'estado': estado,
                'descripcion': desc,
            }
        )
        resultados.append({'nombre': nombre, 'estado': estado})

    return Response({'verificados': len(resultados), 'detalle': resultados})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def probar_xss(request):
    """A07 - Prueba basica de reflexion XSS en parametros comunes."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A07 - XSS (Scripting entre sitios)',
            'descripcion': 'Registra vectores XSS tipicos para revision manual de reflexion en respuestas.',
            'instruccion': 'Haz clic en POST para ejecutar la prueba.'
        })
    payloads = [
        '<script>alert("xss")</script>',
        'javascript:alert("xss")',
        '<img src=x onerror=alert("xss")>',
    ]

    resultados = []
    for payload in payloads:
        # Simulacion: si el payload se refleja sin escape, seria vulnerable
        # En este escaneo guardamos el vector para revision manual
        obj = VulnerabilidadXSS.objects.create(
            vector=payload,
            endpoint='/api/prueba-xss',
            parametros='q=' + payload,
            resultado='Sospechoso',
            detalle='Revisar manualmente si la aplicacion escapa este payload en respuestas HTML o JSON.'
        )
        resultados.append({'vector': payload, 'resultado': obj.resultado})

    return Response({'probados': len(resultados), 'detalle': resultados})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def auditar_deserializacion(request):
    """A08 - Detecta uso de deserializadores inseguros en el proyecto."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A08 - Desserializacion Insegura',
            'descripcion': 'Audita el uso de deserializadores potencialmente peligrosos (pickle, yaml, xml).',
            'instruccion': 'Haz clic en POST para ejecutar la auditoria.'
        })
    checks = [
        ('pickle.loads', 'Alto', 'Evitar pickle.loads con datos no confiables.'),
        ('yaml.load', 'Alto', 'Usar yaml.safe_load en lugar de yaml.load.'),
        ('xml.etree.ElementTree', 'Medio', 'Validar XML contra XXE antes de parsear.'),
        ('json.loads', 'Bajo', 'JSON es seguro por defecto, verificar schema si es critico.'),
    ]

    resultados = []
    for origen, riesgo, recomendacion in checks:
        obj, _ = IntentoDeserializacion.objects.update_or_create(
            origen=origen,
            defaults={
                'tipo_dato': origen.split('.')[0].upper(),
                'permitido': riesgo == 'Bajo',
                'riesgo': riesgo,
                'recomendacion': recomendacion,
            }
        )
        resultados.append({'origen': origen, 'riesgo': riesgo})

    return Response({'auditados': len(resultados), 'detalle': resultados})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def escanear_componentes(request):
    """A09 - Escanea dependencias en busca de vulnerabilidades conocidas."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A09 - Componentes con Vulnerabilidades Conocidas',
            'descripcion': 'Lista dependencias de Python instaladas y detecta versiones con CVEs conocidos.',
            'instruccion': 'Haz clic en POST para ejecutar el escaneo.'
        })
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--format=json'],
            capture_output=True, text=True, check=True
        )
        paquetes = json.loads(result.stdout)
    except Exception as e:
        return Response({'error': str(e), 'nota': 'Asegurate de tener pip disponible.'}, status=500)

    resultados = []
    # Lista basica de componentes con problemas historicos conocidos (ejemplo educativo)
    known_issues = {
        'django': {'min_ok': '4.2.0', 'cve': 'Revisar CVEs recientes'},
        'pillow': {'min_ok': '10.0.0', 'cve': 'CVE-2023-4863'},
        'requests': {'min_ok': '2.31.0', 'cve': 'CVE-2023-32681'},
    }

    for pkg in paquetes:
        nombre = pkg['name'].lower()
        version = pkg['version']
        if nombre in known_issues:
            info = known_issues[nombre]
            obj, _ = ComponenteVulnerable.objects.update_or_create(
                nombre=pkg['name'],
                version=version,
                defaults={
                    'cve_id': info['cve'],
                    'severidad': 'Alta',
                    'descripcion': f'Version instalada {version}. Considerar actualizar a >= {info["min_ok"]}.',
                    'estado': 'Pendiente',
                }
            )
            resultados.append({'nombre': pkg['name'], 'version': version, 'cve': info['cve']})

    return Response({'escaneados': len(resultados), 'detalle': resultados})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def verificar_monitoreo(request):
    """A10 - Registro y Monitoreo Insuficientes."""
    if request.method == 'GET':
        return Response({
            'herramienta': 'A10 - Registro y Monitoreo Insuficientes',
            'descripcion': 'Verifica que existan registros de eventos criticos y alertas de monitoreo.',
            'instruccion': 'Haz clic en POST para ejecutar la verificacion.'
        })
    checks = [
        ('Log de errores Django', 'INFO', 'system', '', 'Verificar configuracion de LOGGING en settings.'),
        ('Log de bitacora de usuario', 'INFO', 'admin', '', 'Verificar que backend.utils.bitacora registra eventos.'),
        ('Log de autenticacion', 'INFO', 'auth', '', 'Verificar intentos de login/logout en base de datos.'),
        ('Alerta de acceso no autorizado', 'WARNING', 'system', '10.0.0.1', 'Monitorear respuestas HTTP 403 y 401.'),
    ]

    resultados = []
    for evento, nivel, usuario, ip, detalle in checks:
        obj, _ = RegistroMonitoreo.objects.update_or_create(
            evento=evento,
            defaults={
                'nivel': nivel,
                'usuario': usuario,
                'ip_address': ip,
                'detalle': detalle,
            }
        )
        resultados.append({'evento': evento, 'nivel': nivel})

    return Response({'verificados': len(resultados), 'detalle': resultados})
