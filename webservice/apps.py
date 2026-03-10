from django.apps import AppConfig


class WebserviceConfig(AppConfig):
    name = 'webservice'
    verbose_name = 'Kaarten'

    def ready(self) -> None:
        from . import signals  # noqa
