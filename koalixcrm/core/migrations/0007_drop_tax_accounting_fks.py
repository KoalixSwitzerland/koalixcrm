# -*- coding: utf-8 -*-
"""CR-2c: drop `account_activa` / `account_passiva` from `core.Tax`.

The linkage between a Tax and its accounting accounts now lives on
`accounting.TaxAccountAssignment`. When `koalixcrm.accounting` is installed,
the migration `accounting.0003_tax_and_category_assignments` runs before
this one (via `run_before`) and copies existing values across. When it is
not installed (WFS fork) this migration still runs and simply drops the
columns — there is no data to migrate.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_pdf_export_process_workspace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tax',
            name='account_activa',
        ),
        migrations.RemoveField(
            model_name='tax',
            name='account_passiva',
        ),
    ]
