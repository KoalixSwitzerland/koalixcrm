# -*- coding: utf-8 -*-
"""CR-9: Add workspace FK to workspace-scoped djangoUserExtension models.

Three-phase migration:
  Phase 1 — AddField nullable workspace_id on the four directly-scoped tables:
             documenttemplate (MTI parent), templateset, userextension,
             crm_textparagraphindocumenttemplate.
             MTI children (InvoiceTemplate, QuotationTemplate, …) inherit via
             join and receive no additional column.
  Phase 2 — Data migration: get-or-create Default Workspace, stamp all rows.
  Phase 3 — AlterField to NOT NULL.

No unique_together changes: none of the affected models had existing
unique constraints to convert.
"""
import django.db.models.deletion
from django.db import migrations, models

SCOPED_MODELS = [
    ('djangoUserExtension', 'documenttemplate'),
    ('djangoUserExtension', 'templateset'),
    ('djangoUserExtension', 'userextension'),
    ('djangoUserExtension', 'textparagraphindocumenttemplate'),
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
        ('djangoUserExtension', '0003_ubl_template_rename'),
        ('core', '0006_pdf_export_process_workspace'),
    ]

    operations = [
        # ── Phase 1: add nullable FK columns ──────────────────────────────
        migrations.AddField(
            model_name='documenttemplate',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='templateset',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='userextension',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='textparagraphindocumenttemplate',
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
            model_name='documenttemplate',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='templateset',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='userextension',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='textparagraphindocumenttemplate',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
    ]
