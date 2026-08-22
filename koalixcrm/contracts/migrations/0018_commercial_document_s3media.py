from django.db import migrations, models

import koalixcrm.core.models.s3_media


class Migration(migrations.Migration):
    """Port CommercialDocumentMedia onto the shared S3Media base.

    Schema only — no data migration. The rename keeps `db_table`
    (`crm_commercialdocumentmedia`), so the table itself is untouched.

    `s3_key` is dropped and `s3_url` becomes the relative object key it used to
    duplicate (WFS ADR-7 / QUAQ2-110): storing an absolute URL bakes the
    endpoint host into the row, which is what made the worker's write-back
    unusable from a browser.
    """

    dependencies = [
        ("contract_object_management", "0017_alter_position_product_type"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CommercialDocumentMedia",
            new_name="CommercialDocumentS3Media",
        ),
        migrations.RemoveField(
            model_name="commercialdocuments3media",
            name="s3_key",
        ),
        migrations.AlterField(
            model_name="commercialdocuments3media",
            name="s3_url",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Relative object key inside the bucket — never an absolute URL.",
                max_length=500,
                validators=[koalixcrm.core.models.s3_media.validate_s3_url_is_relative],
                verbose_name="S3 Key",
            ),
        ),
        migrations.AlterField(
            model_name="commercialdocuments3media",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("uploaded", "Uploaded"),
                    ("processing", "Processing"),
                    ("completed", "Completed"),
                    ("failed", "Failed"),
                ],
                default="pending",
                max_length=20,
                verbose_name="Status",
            ),
        ),
    ]
