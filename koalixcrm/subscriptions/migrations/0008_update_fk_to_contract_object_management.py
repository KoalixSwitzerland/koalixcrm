# Hand-written: Update FK from crm.Contract to contract_object_management.Contract
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_update_fk_to_products_app'),
        ('contract_object_management', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='subscription',
                    name='contract',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract_object_management.contract', verbose_name='Subscription Type'),
                ),
            ],
            database_operations=[],
        ),
    ]
