# -*- coding: utf-8 -*-
"""CR-9: Add workspace FK to all workspace-scoped contracts models.

Three-phase migration:
  Phase 1 — AddField nullable workspace_id on every directly-scoped table.
             MTI children (Invoice, CreditNote, Quotation, DespatchAdvice,
             SalesOrder, PurchaseOrder, PaymentReminder) inherit workspace
             via the CommercialDocument join — no FK added on them.
  Phase 2 — Data migration: stamp all existing rows with Default Workspace.
  Phase 3 — AlterField to NOT NULL.
             No unique_together changes: none of the affected models had
             existing unique constraints that require workspace-scoping.
"""
import django.db.models.deletion
from django.db import migrations, models

SCOPED_MODELS = [
    ('contract_object_management', 'contract'),
    ('contract_object_management', 'commercialdocument'),
    ('contract_object_management', 'commercialdocumentposition'),
    ('contract_object_management', 'textparagraphincommercialdocument'),
    ('contract_object_management', 'commercialdocumentmedia'),
    ('contract_object_management', 'postaladdressforcontract'),
    ('contract_object_management', 'phoneaddressforcontract'),
    ('contract_object_management', 'emailaddressforcontract'),
]


def stamp_default_workspace(apps, schema_editor):
    Workspace = apps.get_model('core', 'Workspace')
    ws, _ = Workspace.objects.get_or_create(
        name='Default Workspace',
        defaults={'is_active': True},
    )
    for app_label, model_name in SCOPED_MODELS:
        Model = apps.get_model(app_label, model_name)
        Model.objects.filter(workspace_id__isnull=True).update(workspace_id=ws.id)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contract_object_management', '0010_drop_legacy_customer_fks'),
        ('core', '0006_pdf_export_process_workspace'),
        ('products', '0005_workspace_scoping'),
    ]

    operations = [
        # ── Phase 1: add nullable FK columns ──────────────────────────────
        migrations.AddField(
            model_name='contract',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='commercialdocument',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='commercialdocumentposition',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='textparagraphincommercialdocument',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='commercialdocumentmedia',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='postaladdressforcontract',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='phoneaddressforcontract',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='emailaddressforcontract',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),

        # ── Phase 2: stamp existing rows ──────────────────────────────────
        migrations.RunPython(stamp_default_workspace, noop),

        # ── Phase 3: make NOT NULL ─────────────────────────────────────────
        migrations.AlterField(
            model_name='contract',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='commercialdocument',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='commercialdocumentposition',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='textparagraphincommercialdocument',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='commercialdocumentmedia',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='postaladdressforcontract',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='phoneaddressforcontract',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='emailaddressforcontract',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
    ]
