from django.apps import AppConfig


class PartidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.partidos'

    def ready(self):
        import backend.partidos.signals  # noqa: F401
