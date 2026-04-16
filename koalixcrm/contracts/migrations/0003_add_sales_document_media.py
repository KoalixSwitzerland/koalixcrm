# Generated manually — adds SalesDocumentMedia model

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from koalixcrm.migration_utils import CreateModelIfNotExists


def cleanup_orphaned_admin_log(apps, schema_editor):
    """
    Delete django_admin_log rows that reference content types which no longer
    exist.  This is a pre-existing data-integrity issue (unrelated to this
    migration) that causes SQLite's check_constraints() to fail on every
    subsequent migration.
    """
    cursor = schema_editor.connection.cursor()
    cursor.execute(
        "DELETE FROM django_admin_log "
        "WHERE content_type_id NOT IN (SELECT id FROM django_content_type)"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("contract_object_management", "0002_initial"),
        ("core", "0004_pdf_export_process"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Fix orphaned FK rows that block SQLite constraint checks
        migrations.RunPython(
            cleanup_orphaned_admin_log,
            migrations.RunPython.noop,
        ),
        CreateModelIfNotExists(
            name="SalesDocumentMedia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "s3_url",
                    models.CharField(
                        help_text="Full URL to the file in S3 / MinIO",
                        max_length=500,
                        verbose_name="S3 URL",
                    ),
                ),
                (
                    "s3_key",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Object key inside the S3 bucket",
                        max_length=500,
                        verbose_name="S3 Key",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "media_type",
                    models.CharField(
                        default="application/pdf",
                        help_text="MIME type of the stored file",
                        max_length=50,
                        verbose_name="Media Type",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Created At",
                    ),
                ),
                (
                    "last_updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="Last Updated At",
                    ),
                ),
                (
                    "sales_document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media_files",
                        to="contract_object_management.salesdocument",
                        verbose_name="Sales Document",
                    ),
                ),
                (
                    "pdf_export_process",
                    models.ForeignKey(
                        blank=True,
                        help_text="The async export process that created this media",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="media_files",
                        to="core.pdfexportprocess",
                        verbose_name="PDF Export Process",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_sales_document_media",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sales Document Media",
                "verbose_name_plural": "Sales Document Media",
                "db_table": "crm_salesdocumentmedia",
                "ordering": ["-created_at"],
            },
        ),
    ]
