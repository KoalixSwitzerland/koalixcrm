# Generated migration for koalixcrm core app — PDFExportProcess table.
# Lives in its own migration (not core.0001_initial) because the legacy
# 2019-era DB doesn't have crm_pdfexportprocess, and mixing it with the
# legacy-present Currency/Unit/Tax tables would prevent
# sync_split_migrations from auto-recording core.0001_initial on upgrade.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


from koalixcrm.migration_utils import CreateModelIfNotExists


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_pdf_export_process_links'),
        ('djangoUserExtension', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        CreateModelIfNotExists(
            name='PDFExportProcess',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('source_model', models.CharField(help_text='Class name of the source object (e.g. Invoice, Quotation)', max_length=100, verbose_name='Source Model')),
                ('source_id', models.BigIntegerField(verbose_name='Source Object ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20, verbose_name='Status')),
                ('result_url', models.URLField(blank=True, default='', help_text='S3 URL of the generated PDF', max_length=500, verbose_name='Result URL')),
                ('error_message', models.TextField(blank=True, default='', verbose_name='Error Message')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('template_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djangoUserExtension.documenttemplate', verbose_name='Template Set')),
                ('triggered_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Triggered By')),
            ],
            options={
                'verbose_name': 'PDF Export Process',
                'verbose_name_plural': 'PDF Export Processes',
                'ordering': ['-created_at'],
                'db_table': 'crm_pdfexportprocess',
            },
        ),
    ]
