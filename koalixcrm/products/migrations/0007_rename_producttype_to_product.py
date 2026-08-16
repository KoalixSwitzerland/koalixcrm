# -*- coding: utf-8 -*-
"""ADR-0003 Amendment 2026-06-27 — v2.0.0 breaking cut.

`ProductType` (the data-bearing model: title, internal number, unit, tax)
is renamed to `Product`. Primary keys are preserved; FK constraints from
`contracts`, `accounting`, `core` (UnitTransform/CurrencyTransform) and
`subscriptions` follow the rename automatically via Django's
`RenameModel` project-state propagation — no per-row FK rewrite, no new
migrations required in those apps (verification points (a)/(c), see
products-app engineering report).

The previous, semantically empty `Product` identifier-hull model is
removed in the same migration; nothing in the codebase held an incoming
FK to it (verification point (b) — confirmed empty at implementation
time), so no rewire to `ProductVariant` was necessary at the database
level.

Database operations:
  1. DROP TABLE crm_product (the hollow hull).
  2. ALTER TABLE crm_producttype RENAME TO products_product (pure rename,
     `SeparateDatabaseAndState` so the state-side `RenameModel` differs
     from the literal SQL).

`kind` is added in the same migration with `TRADING_GOOD` as the backfill
default for migrated rows (least-restrictive value: requires neither a
`ServiceProfile` nor a `BillOfMaterials`); the model itself carries no
Python-level default, so newly created rows must set `kind` explicitly.
Reversible: `RunPython.noop`/`RunSQL` reverse pairs restore the pre-rename
schema exactly, and the state operations mirror in `RenameModel`'s
built-in reversibility.
"""
from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_drop_accounting_product_category'),
        # Force every pre-existing migration in other apps that hardcodes a
        # literal 'products.ProductType'/'products.producttype' string FK
        # reference (contract_object_management 0002/0012, accounting 0003,
        # subscriptions 0001, core 0002) to apply *before* the rename. Django's
        # RenameModel state propagation only rewrites FK references already
        # present in the project state at the time it runs; a same-named
        # literal string in a migration that executes *after* the rename
        # cannot resolve and raises `AttributeError` at migrate time. Without
        # these explicit edges the cross-app topological order is otherwise
        # unconstrained and can flip depending on what else has been added to
        # the graph.
        ('contract_object_management', '0016_remove_commercialdocumentmedia_pdf_export_process_and_more'),
        ('accounting', '0003_tax_and_category_assignments'),
        ('subscriptions', '0001_initial'),
        ('core', '0008_remove_roleinworkspace_crm_riw_group_ws_idx_and_more'),
    ]

    operations = [
        # ── 1. Drop the hollow identifier-hull `Product` model ──────────
        migrations.DeleteModel(
            name='Product',
        ),
        # ── 2. Rename ProductType -> Product (state) / pure table rename (db) ──
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameModel(
                    old_name='ProductType',
                    new_name='Product',
                ),
                migrations.AlterModelTable(
                    name='product',
                    table='products_product',
                ),
                migrations.AlterModelOptions(
                    name='product',
                    options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql="ALTER TABLE crm_producttype RENAME TO products_product",
                    reverse_sql="ALTER TABLE products_product RENAME TO crm_producttype",
                ),
            ],
        ),
        # ── 3. `kind` — default TRADING_GOOD for migrated rows (OQ-0008) ──
        migrations.AddField(
            model_name='product',
            name='kind',
            field=models.CharField(
                choices=[
                    ('SERVICE', 'Service'),
                    ('TRADING_GOOD', 'Trading Good'),
                    ('MANUFACTURED_GOOD', 'Manufactured Good'),
                    ('KIT', 'Kit'),
                    ('RAW_MATERIAL', 'Raw Material'),
                ],
                default='TRADING_GOOD',
                max_length=32,
                verbose_name='Kind',
            ),
            preserve_default=False,
        ),
    ]
