# Generated migration for koalixcrm settings app

import django.db.models.deletion
from django.db import migrations, models


from koalixcrm.migration_utils import CreateModelIfNotExists


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        CreateModelIfNotExists(
            name='CurrencyTransform',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('factor', models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Factor between From and To Currency')),
                ('from_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='db_reltransformfromcurrency', to='settings.currency', verbose_name='From Currency')),
                ('to_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='db_reltransformtocurrency', to='settings.currency', verbose_name='To Currency')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.producttype', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Currency Transform',
                'verbose_name_plural': 'Currency Transforms',
                'db_table': 'crm_currencytransform',
            },
        ),
        CreateModelIfNotExists(
            name='UnitTransform',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('factor', models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Factor between From and To Unit')),
                ('from_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='db_reltransfromfromunit', to='settings.unit', verbose_name='From Unit')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.producttype', verbose_name='Product Type')),
                ('to_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='db_reltransfromtounit', to='settings.unit', verbose_name='To Unit')),
            ],
            options={
                'verbose_name': 'Unit Transform',
                'verbose_name_plural': 'Unit Transforms',
                'db_table': 'crm_unittransform',
            },
        ),
    ]
