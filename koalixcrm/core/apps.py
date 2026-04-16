# -*- coding: utf-8 -*-
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'koalixcrm.core'
    label = 'core'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import koalixcrm.core.signals.pdf_export_signals  # noqa: F401
