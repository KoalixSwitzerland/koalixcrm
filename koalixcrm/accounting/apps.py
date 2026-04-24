from django.apps import AppConfig


class AccountingConfig(AppConfig):
    name = 'koalixcrm.accounting'
    label = 'accounting'
    default_auto_field = 'django.db.models.BigAutoField'
    required_peers: tuple[str, ...] = ('koalixcrm.core', 'koalixcrm.djangoUserExtension')
    optional_peers: tuple[str, ...] = ('koalixcrm.products',)

    def ready(self):
        from koalixcrm.core.app_checks import register_peer_check
        register_peer_check(self)
        from koalixcrm.accounting import admin_hooks  # noqa: F401
