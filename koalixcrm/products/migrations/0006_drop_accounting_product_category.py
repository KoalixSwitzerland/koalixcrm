# -*- coding: utf-8 -*-
"""CR-2c: drop `accounting_product_category` from `products.ProductType`.

The linkage now lives on `accounting.ProductCategoryAssignment`. Dual-path
semantics mirror `core.0007_drop_tax_accounting_fks`.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_workspace_scoping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producttype',
            name='accounting_product_category',
        ),
    ]
