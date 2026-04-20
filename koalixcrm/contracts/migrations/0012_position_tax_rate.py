# -*- coding: utf-8 -*-
"""CR-2: position-level tax-rate fallback + relax product_type blank.

When the `products` app is not installed (or simply not linked on a given
position), the position must still be able to describe its own tax rate.
This migration:

- Adds `position_tax_rate` to `Position` and `CommercialDocumentPosition`.
- Widens `product_type.blank` so admin/forms accept positions without a
  product type. The column was already `null=True`.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_object_management', '0011_workspace_scoping'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='position_tax_rate',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text=(
                    'Used for tax calculation when no product type is set '
                    'on the position.'
                ),
                max_digits=5,
                null=True,
                verbose_name='Tax Rate (%)',
            ),
        ),
        migrations.AlterField(
            model_name='position',
            name='product_type',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                to='products.producttype',
                verbose_name='Product',
            ),
        ),
    ]
