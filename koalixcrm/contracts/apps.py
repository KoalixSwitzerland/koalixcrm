# -*- coding: utf-8 -*-
from django.apps import AppConfig


class ContractObjectManagementConfig(AppConfig):
    name = 'koalixcrm.contracts'
    label = 'contract_object_management'
    default_auto_field = 'django.db.models.BigAutoField'
    required_peers: tuple[str, ...] = ('koalixcrm.core', 'koalixcrm.contacts')
    optional_peers: tuple[str, ...] = (
        'koalixcrm.products',
        'koalixcrm.djangoUserExtension',
    )

    def ready(self):
        from koalixcrm.core.app_checks import register_peer_check
        register_peer_check(self)
