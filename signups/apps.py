from django.apps import AppConfig


class SignupsConfig(AppConfig):
    name = 'signups'

    def ready(self):
        import signups.signals  # noqa
