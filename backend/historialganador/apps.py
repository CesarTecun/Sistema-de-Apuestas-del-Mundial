from django.apps import AppConfig


class HistorialganadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.historialganador'
    verbose_name = 'Historial Ganador'

    def ready(self):
        """Importar señales cuando la app esté lista"""
        import backend.historialganador.signals
