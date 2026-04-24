# -*- coding: utf-8 -*-
"""CR-9: Add workspace FK to all workspace-scoped contacts models.

Three-phase migration:
  Phase 1 — AddField nullable workspace_id on every affected table.
  Phase 2 — Data migration: stamp all existing rows with Default Workspace.
  Phase 3 — AlterField to NOT NULL (no unique_together changes needed because
             no contacts model had existing unique constraints).
"""
import django.db.models.deletion
from django.db import migrations, models

# Tables that receive a workspace column directly (MTI children excluded).
SCOPED_MODELS = [
    'party',
    'partygroup',
    'address',
    'phonenumber',
    'partyemail',
    'customerbillingcycle',
    'partyrole',
    'partyidentification',
    'organizationmembership',
    'organizationrelationship',
    'addressassignment',
    'phoneassignment',
    'emailassignment',
    'partygroupmembership',
]


def stamp_default_workspace(apps, schema_editor):
    Workspace = apps.get_model('core', 'Workspace')
    ws, _ = Workspace.objects.get_or_create(
        name='Default Workspace',
        defaults={'is_active': True},
    )
    for model_name in SCOPED_MODELS:
        Model = apps.get_model('contacts', model_name)
        Model.objects.filter(workspace_id__isnull=True).update(workspace_id=ws.id)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0010_drop_partycontact_preferred_language'),
        ('core', '0006_pdf_export_process_workspace'),
    ]

    operations = [
        # ── Phase 1: add nullable FK columns ──────────────────────────────
        migrations.AddField(
            model_name='party',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='partygroup',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='address',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='partyemail',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='customerbillingcycle',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='partyrole',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='partyidentification',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='organizationmembership',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='organizationrelationship',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='addressassignment',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='phoneassignment',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='emailassignment',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AddField(
            model_name='partygroupmembership',
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
            model_name='party',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='partygroup',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='address',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='partyemail',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='customerbillingcycle',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='partyrole',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='partyidentification',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='organizationmembership',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='organizationrelationship',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='addressassignment',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='phoneassignment',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='emailassignment',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
        migrations.AlterField(
            model_name='partygroupmembership',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
            ),
        ),
    ]
