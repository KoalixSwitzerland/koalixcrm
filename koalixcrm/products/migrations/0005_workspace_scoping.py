# -*- coding: utf-8 -*-
"""CR-9: Add workspace FK to all workspace-scoped products models.

Three-phase migration:
  Phase 1 — AddField nullable workspace_id on each directly-scoped table.
             (crm_price is the MTI parent; crm_productprice inherits via join.)
  Phase 2 — Data migration: stamp all existing rows with Default Workspace.
  Phase 3 — AlterField to NOT NULL (no unique_together changes — no existing
             unique constraints on these models).
"""
import django.db.models.deletion
from django.db import migrations, models


SCOPED_MODELS = [
    ('producttype', 'crm_producttype'),
    ('product', 'crm_product'),
    ('price', 'crm_price'),
    ('customergrouptransform', 'crm_customergrouptransform'),
]


def stamp_default_workspace(apps, schema_editor):
    Workspace = apps.get_model('core', 'Workspace')
    ws, _ = Workspace.objects.get_or_create(
        name='Default Workspace',
        defaults={'is_active': True},
    )
    for model_name, _table in SCOPED_MODELS:
        Model = apps.get_model('products', model_name)
        Model.objects.filter(workspace_id__isnull=True).update(workspace_id=ws.id)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_drop_legacy_customer_group_fks'),
        ('core', '0006_pdf_export_process_workspace'),
    ]

    operations = [
        # ── Phase 1: add nullable FK columns ──────────────────────────────
        migrations.AddField(
            model_name='producttype',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='price',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='customergrouptransform',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        # ── Phase 2: data migration ────────────────────────────────────────
        migrations.RunPython(stamp_default_workspace, noop),
        # ── Phase 3: make NOT NULL ─────────────────────────────────────────
        migrations.AlterField(
            model_name='producttype',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='price',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='customergrouptransform',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
    ]
