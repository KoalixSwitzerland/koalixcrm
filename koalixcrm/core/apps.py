# -*- coding: utf-8 -*-
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'koalixcrm.core'
    label = 'core'
    default_auto_field = 'django.db.models.BigAutoField'
    required_peers: tuple[str, ...] = ()
    optional_peers: tuple[str, ...] = ('koalixcrm.accounting',)

    def ready(self):
        import koalixcrm.core.signals.pdf_export_signals  # noqa: F401
        from koalixcrm.core.app_checks import register_peer_check
        register_peer_check(self)
