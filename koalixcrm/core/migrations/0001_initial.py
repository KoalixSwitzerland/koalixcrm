# Generated migration for koalixcrm core app

import django.db.models.deletion
from django.db import migrations, models


from koalixcrm.migration_utils import CreateModelIfNotExists


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        CreateModelIfNotExists(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
                ('short_name', models.CharField(max_length=3, verbose_name='Displayed Name After Prices')),
                ('rounding', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Rounding')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currency',
                'db_table': 'crm_currency',
            },
        ),
        CreateModelIfNotExists(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
                ('short_name', models.CharField(max_length=3, verbose_name='Displayed Name After Quantity In The Position')),
                ('fraction_factor_to_next_higher_unit', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True, verbose_name='Factor Between This And Next Higher Unit')),
                ('is_a_fraction_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.unit', verbose_name='Is A Fraction Of')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
                'db_table': 'crm_unit',
            },
        ),
        CreateModelIfNotExists(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Taxrate in Percentage')),
                ('name', models.CharField(max_length=100, verbose_name='Taxname')),
                ('account_activa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='db_relaccountactiva', to='accounting.account', verbose_name='Activa Account')),
                ('account_passiva', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='db_relaccountpassiva', to='accounting.account', verbose_name='Passiva Account')),
            ],
            options={
                'verbose_name': 'Tax',
                'verbose_name_plural': 'Taxes',
                'db_table': 'crm_tax',
            },
        ),
    ]
