from django.apps import AppConfig


class DjangoUserExtensionConfig(AppConfig):
    name = 'koalixcrm.djangoUserExtension'
    label = 'djangoUserExtension'
    default_auto_field = 'django.db.models.BigAutoField'
    required_peers: tuple[str, ...] = ('koalixcrm.core', 'koalixcrm.contacts')
    optional_peers: tuple[str, ...] = ('koalixcrm.reporting',)

    def ready(self):
        from koalixcrm.core.app_checks import register_peer_check
        register_peer_check(self)
