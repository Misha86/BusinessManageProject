from django.apps import AppConfig


class BusinessConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        """Implicitly connect a signal handlers decorated with @receiver."""
        from . import signals
