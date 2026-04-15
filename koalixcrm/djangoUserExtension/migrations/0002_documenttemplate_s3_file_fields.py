# Generated manually — migrate DocumentTemplate from FileBrowseField to FileField with S3 storage

from django.db import migrations, models
import koalixcrm_utils.s3_storage


class Migration(migrations.Migration):

    dependencies = [
        ("djangoUserExtension", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documenttemplate",
            name="xsl_file",
            field=models.FileField(
                max_length=200,
                storage=koalixcrm_utils.s3_storage.TemplateFileStorage,
                upload_to="xsl/",
                verbose_name="XSL File",
            ),
        ),
        migrations.AlterField(
            model_name="documenttemplate",
            name="fop_config_file",
            field=models.FileField(
                blank=True,
                max_length=200,
                null=True,
                storage=koalixcrm_utils.s3_storage.TemplateFileStorage,
                upload_to="fop_config/",
                verbose_name="FOP Configuration File",
            ),
        ),
        migrations.AlterField(
            model_name="documenttemplate",
            name="logo",
            field=models.FileField(
                blank=True,
                max_length=200,
                null=True,
                storage=koalixcrm_utils.s3_storage.TemplateFileStorage,
                upload_to="logos/",
                verbose_name="Logo for the PDF generation",
            ),
        ),
    ]
