from django.db import migrations, models

from koalixcrm.migration_utils import AddFieldIfNotExists


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_initial'),
    ]

    operations = [
        AddFieldIfNotExists(
            model_name='postaladdress',
            name='subdivision_code',
            field=models.CharField(
                blank=True,
                help_text='e.g. ZH for Kanton Zürich, BY for Bayern — used for regional public holidays',
                max_length=3,
                null=True,
                verbose_name='Subdivision Code (ISO 3166-2 suffix)',
            ),
        ),
    ]
