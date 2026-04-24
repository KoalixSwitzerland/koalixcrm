# -*- coding: utf-8 -*-
"""CR-2c: relocate accounting FKs off `core.Tax` and `products.ProductType`.

This migration
  1. creates the accounting-owned assignment tables,
  2. copies existing linkage rows from the source tables into the new ones,
  3. runs *before* `core.0007_drop_tax_accounting_fks` and
     `products.0006_drop_accounting_product_category`.

The `run_before` dependency is conditional on this migration actually being
applied: if `koalixcrm.accounting` is not installed (WFS fork), the two
destination-app drops simply run without a preceding data copy — there is
no data to lose because the source rows never existed in that deployment.
"""
import django.db.models.deletion
from django.db import migrations, models


def _copy_tax_account_fks(apps, schema_editor):
    Tax = apps.get_model('core', 'Tax')
    TaxAccountAssignment = apps.get_model('accounting', 'TaxAccountAssignment')
    for tax in Tax.objects.all():
        activa_id = getattr(tax, 'account_activa_id', None)
        passiva_id = getattr(tax, 'account_passiva_id', None)
        if activa_id is None and passiva_id is None:
            continue
        TaxAccountAssignment.objects.update_or_create(
            tax=tax,
            defaults={
                'activa_account_id': activa_id,
                'passiva_account_id': passiva_id,
            },
        )


def _copy_product_category_fks(apps, schema_editor):
    ProductType = apps.get_model('products', 'ProductType')
    ProductCategoryAssignment = apps.get_model('accounting', 'ProductCategoryAssignment')
    for product_type in ProductType.objects.all():
        category_id = getattr(product_type, 'accounting_product_category_id', None)
        if category_id is None:
            continue
        ProductCategoryAssignment.objects.update_or_create(
            product_type=product_type,
            defaults={'category_id': category_id},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_initial'),
        ('core', '0006_pdf_export_process_workspace'),
        ('products', '0005_workspace_scoping'),
    ]

    run_before = [
        ('core', '0007_drop_tax_accounting_fks'),
        ('products', '0006_drop_accounting_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxAccountAssignment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tax', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='account_assignment',
                    to='core.tax',
                    verbose_name='Tax',
                )),
                ('activa_account', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tax_account_assignments_as_activa',
                    to='accounting.account',
                    verbose_name='Activa Account',
                )),
                ('passiva_account', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tax_account_assignments_as_passiva',
                    to='accounting.account',
                    verbose_name='Passiva Account',
                )),
            ],
            options={
                'verbose_name': 'Tax Account Assignment',
                'verbose_name_plural': 'Tax Account Assignments',
            },
        ),
        migrations.CreateModel(
            name='ProductCategoryAssignment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_type', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='product_category_assignment',
                    to='products.producttype',
                    verbose_name='Product Type',
                )),
                ('category', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='product_type_assignments',
                    to='accounting.productcategory',
                    verbose_name='Accounting Product Category',
                )),
            ],
            options={
                'verbose_name': 'Product Category Assignment',
                'verbose_name_plural': 'Product Category Assignments',
            },
        ),
        migrations.RunPython(_copy_tax_account_fks, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(_copy_product_category_fks, reverse_code=migrations.RunPython.noop),
    ]
