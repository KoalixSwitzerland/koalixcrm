from django.db import migrations, models


class Migration(migrations.Migration):
    """Widen `PDFExportProcess.result_url` from URLField to CharField.

    The column type is unchanged (both are varchar(500)); only the validators
    differ. Django's URLValidator requires a TLD or `localhost`, so it rejects
    the container-network URLs the PDF worker reports (`http://minio:9000/...`)
    and the status write-back fails with 400. The value is machine-generated,
    never user input — same as `CommercialDocumentS3Media.s3_url`, which is
    already a CharField.
    """

    dependencies = [
        ("core", "0009_alter_unittransform_product_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pdfexportprocess",
            name="result_url",
            field=models.CharField(
                blank=True,
                default="",
                help_text="S3 URL of the generated PDF",
                max_length=500,
                verbose_name="Result URL",
            ),
        ),
    ]
