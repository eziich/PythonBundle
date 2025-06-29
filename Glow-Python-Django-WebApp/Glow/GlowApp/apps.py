
from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    name = 'GlowApp'

    def ready(self):
        import Glow.GlowApp.signals



class GlowappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GlowApp'
