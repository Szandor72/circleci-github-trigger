from __future__ import unicode_literals

from django.apps import AppConfig


class TriggersConfig(AppConfig):
    name = 'triggers'

    def ready(self):
        import triggers.handlers
