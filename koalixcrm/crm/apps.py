from django.apps import AppConfig


class CrmConfig(AppConfig):
    name = 'koalixcrm.crm'
    label = 'crm'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import koalixcrm.crm.signals.pdf_export_signals  # noqa: F401
