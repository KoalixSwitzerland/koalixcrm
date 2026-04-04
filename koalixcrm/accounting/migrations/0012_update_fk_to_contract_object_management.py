# Hand-written: Update FK from crm.Invoice to contract_object_management.Invoice
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0011_auto_20240329_2207'),
        ('contract_object_management', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='booking',
                    name='booking_reference',
                    field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contract_object_management.invoice', verbose_name='Booking Reference'),
                ),
            ],
            database_operations=[],
        ),
    ]
