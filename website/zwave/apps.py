from django.apps import AppConfig

class ZWaveAppConfig(AppConfig):
    name = 'website.zwave'

    def ready(self):
        import website.zwave.signals