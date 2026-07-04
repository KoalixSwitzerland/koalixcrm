# -*- coding: utf-8 -*-
from __future__ import annotations

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'koalixcrm.products'
    label = 'products'
    default_auto_field = 'django.db.models.BigAutoField'
    required_peers: tuple[str, ...] = ('koalixcrm.core',)
    optional_peers: tuple[str, ...] = ('koalixcrm.accounting',)

    def ready(self) -> None:
        from koalixcrm.core.app_checks import register_peer_check
        register_peer_check(self)

        from koalixcrm.products.signals.attribute_mirror import (
            register_attribute_mirror_signals,
        )
        register_attribute_mirror_signals()

        from koalixcrm.products.signals.bom_version import register_bom_version_signals
        register_bom_version_signals()

        from koalixcrm.products.services.kind_lock_providers import (
            register_stage3_lock_providers,
        )
        register_stage3_lock_providers()
