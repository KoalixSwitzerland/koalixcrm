# -*- coding: utf-8 -*-
from __future__ import annotations

from django.apps import AppConfig


class StockConfig(AppConfig):
    name = 'koalixcrm.stock'
    label = 'stock'
    default_auto_field = 'django.db.models.BigAutoField'
    required_peers: tuple[str, ...] = ('koalixcrm.core', 'koalixcrm.products')
    optional_peers: tuple[str, ...] = ('koalixcrm.contacts',)

    def ready(self) -> None:
        from koalixcrm.core.app_checks import register_peer_check
        register_peer_check(self)

        from koalixcrm.stock.services.kind_lock_providers import (
            register_stock_lock_providers,
        )
        register_stock_lock_providers()
