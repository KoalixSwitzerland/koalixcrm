# Hand-written: Update FK from crm.ProductType to products.ProductType
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_auto_20240329_2207'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='subscriptiontype',
                    name='product_type',
                    field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.producttype', verbose_name='Product Type'),
                ),
            ],
            database_operations=[],
        ),
    ]
