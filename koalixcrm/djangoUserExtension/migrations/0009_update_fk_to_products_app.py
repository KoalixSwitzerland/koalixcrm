# Hand-written: Update FK from crm.Currency to products.Currency
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoUserExtension', '0008_auto_20240329_2207'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='userextension',
                    name='default_currency',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.currency'),
                ),
            ],
            database_operations=[],
        ),
    ]
