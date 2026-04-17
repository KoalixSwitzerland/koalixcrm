# Generated migration for koalixcrm core app — PDFExportProcess cross-app FKs

from django.conf import settings
from django.db import migrations




class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_transforms'),
        ('djangoUserExtension', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Intentionally empty: forces core.0001_initial to be a parent of
        # contact_object_management.0003_add_sales_document_media without
        # modeling a concrete schema change. PDFExportProcess itself is
        # created by core.0004_pdf_export_process (which depends on this
        # migration), so that sync_split_migrations can auto-record
        # core.0001_initial on legacy DBs that don't yet have the
        # crm_pdfexportprocess table.
    ]
