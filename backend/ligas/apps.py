from django.apps import AppConfig


class LigasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.ligas'

    def ready(self):
        """Importar signals cuando la app esté lista"""
        import backend.ligas.signals
