# Hand-written migration: Remove product models from crm state (moved to products app)
# No database operations - tables stay as crm_* with db_table setting

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0059_auto_20240329_2207'),
        ('products', '0001_initial'),
    ]

    operations = [
        # First update FK references on models staying in crm to point to products app
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # Update FKs on Contract
                migrations.AlterField(
                    model_name='contract',
                    name='default_currency',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.currency', verbose_name='Default Currency'),
                ),
                # Update FKs on SalesDocument
                migrations.AlterField(
                    model_name='salesdocument',
                    name='currency',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.currency', verbose_name='Currency'),
                ),
                # Update FKs on Position/SalesDocumentPosition
                migrations.AlterField(
                    model_name='position',
                    name='product_type',
                    field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.producttype', verbose_name='Product'),
                ),
                migrations.AlterField(
                    model_name='position',
                    name='unit',
                    field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.unit', verbose_name='Unit'),
                ),
                # Update FKs on Agreement
                migrations.AlterField(
                    model_name='agreement',
                    name='unit',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.unit'),
                ),
                # Update FKs on Project
                migrations.AlterField(
                    model_name='project',
                    name='default_currency',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.currency', verbose_name='Default Currency'),
                ),
                # Update FK on ResourcePrice (inherits from Price, price_ptr now points to products.price)
                migrations.AlterField(
                    model_name='resourceprice',
                    name='price_ptr',
                    field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.price'),
                ),
            ],
            database_operations=[],
        ),
        # Now remove product models from crm state (dependents first)
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='ProductPrice'),
                migrations.DeleteModel(name='CurrencyTransform'),
                migrations.DeleteModel(name='UnitTransform'),
                migrations.DeleteModel(name='CustomerGroupTransform'),
                migrations.DeleteModel(name='Product'),
                migrations.DeleteModel(name='Price'),
                migrations.DeleteModel(name='ProductType'),
                migrations.DeleteModel(name='Currency'),
                migrations.DeleteModel(name='Unit'),
                migrations.DeleteModel(name='Tax'),
            ],
            database_operations=[],
        ),
    ]
