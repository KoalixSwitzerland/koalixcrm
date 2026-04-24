# -*- coding: utf-8 -*-
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'koalixcrm.products'
    label = 'products'
    default_auto_field = 'django.db.models.BigAutoField'
    required_peers: tuple[str, ...] = ('koalixcrm.core',)
    optional_peers: tuple[str, ...] = ('koalixcrm.accounting',)

    def ready(self):
        from koalixcrm.core.app_checks import register_peer_check
        register_peer_check(self)
