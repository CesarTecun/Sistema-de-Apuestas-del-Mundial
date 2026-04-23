import uuid
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .models import SesionUsuario


class SesionTrackingMiddleware(MiddlewareMixin):
    """
    Middleware para rastrear sesiones de usuarios en tiempo real.
    Captura:
    - Inicio de sesión
    - Actividad del usuario (última actividad)
    - Cierre de sesión
    - IP y dispositivo
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        """
        Procesa cada request para actualizar actividad de sesión.
        Se ejecuta en cada petición del usuario autenticado.
        """
        # Solo procesar si el usuario está autenticado
        if hasattr(request, 'user') and request.user.is_authenticated:
            self._actualizar_actividad_sesion(request)

    def process_response(self, request, response):
        """
        Procesa la respuesta (placeholder para futuras extensiones).
        """
        return response

    def _actualizar_actividad_sesion(self, request):
        """
        Actualiza la última actividad de la sesión activa del usuario.
        """
        try:
            # Buscar sesión activa del usuario
            sesion = SesionUsuario.objects.filter(
                fk_id_usuario=request.user.id_usuario,
                estado_sesion='Activa'
            ).order_by('-fecha_ultima_actividad').first()

            if sesion:
                # Actualizar última actividad
                sesion.fecha_ultima_actividad = timezone.now()
                sesion.save(update_fields=['fecha_ultima_actividad'])

        except Exception:
            # Silenciar errores para no afectar la experiencia del usuario
            pass


class SesionInicioMiddleware(MiddlewareMixin):
    """
    Middleware especializado para capturar el inicio de sesión.
    Se ejecuta después del login exitoso.
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Detecta cuando se accede a la vista de login exitosa.
        """
        # Verificar si es la vista de login y fue exitoso
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Verificar si ya existe sesión activa para este request
            if not getattr(request, '_sesion_creada', False):
                self._crear_sesion(request)
                request._sesion_creada = True

    def _crear_sesion(self, request):
        """
        Crea un nuevo registro de sesión para el usuario.
        """
        try:
            # Obtener información del request
            ip_address = self._get_ip_address(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            dispositivo = self._detectar_dispositivo(user_agent)

            # Generar token de sesión único
            token_sesion = str(uuid.uuid4())

            # Crear sesión en la base de datos
            SesionUsuario.objects.create(
                fk_id_usuario=request.user.id_usuario,
                token_sesion=token_sesion,
                estado_sesion='Activa',
                ip_address=ip_address,
                user_agent=user_agent,
                dispositivo=dispositivo
            )

            # Guardar token en session de Django para referencia
            request.session['token_sesion'] = token_sesion

        except Exception:
            pass

    def _get_ip_address(self, request):
        """
        Obtiene la dirección IP del usuario.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip[:45] if ip else None

    def _detectar_dispositivo(self, user_agent):
        """
        Detecta el tipo de dispositivo basado en el user agent.
        """
        user_agent_lower = user_agent.lower()

        if 'mobile' in user_agent_lower or 'android' in user_agent_lower or 'iphone' in user_agent_lower:
            return 'Móvil'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'Tablet'
        elif 'windows' in user_agent_lower or 'macintosh' in user_agent_lower or 'linux' in user_agent_lower:
            return 'Escritorio'
        else:
            return 'Desconocido'
