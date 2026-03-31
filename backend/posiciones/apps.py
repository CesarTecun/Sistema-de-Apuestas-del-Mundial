from django.apps import AppConfig


class PosicionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.posiciones'
    verbose_name = 'Posiciones'

    def ready(self):
        """Importar señales cuando la app esté lista"""
        import backend.posiciones.signals
