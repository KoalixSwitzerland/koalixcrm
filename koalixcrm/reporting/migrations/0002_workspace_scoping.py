# -*- coding: utf-8 -*-
"""Add workspace FK to all workspace-scoped reporting models.

Three-phase migration:
  Phase 1 — AddField nullable workspace_id on every directly-scoped table.
             HumanResource is MTI on Resource, so it inherits workspace via
             the parent join — no FK added on it. ResourcePrice is MTI on
             products.Price, which is already workspace-scoped.
  Phase 2 — Data migration: stamp all existing rows with Default Workspace.
  Phase 3 — AlterField to NOT NULL.

Status / type / link-type lookup tables (ProjectStatus, TaskStatus,
ReportingPeriodStatus, EstimationStatus, AgreementStatus, AgreementType,
ResourceType, ProjectLinkType, TaskLinkType) are intentionally left as
global reference data and are NOT lifted by this migration.
"""
import django.db.models.deletion
from django.db import migrations, models

SCOPED_MODELS = [
    ('reporting', 'project'),
    ('reporting', 'task'),
    ('reporting', 'reportingperiod'),
    ('reporting', 'work'),
    ('reporting', 'resource'),
    ('reporting', 'resourcemanager'),
    ('reporting', 'agreement'),
    ('reporting', 'estimation'),
    ('reporting', 'genericprojectlink'),
    ('reporting', 'generictasklink'),
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
        ('reporting', '0001_initial'),
        ('core', '0006_pdf_export_process_workspace'),
    ]

    operations = (
        # ── Phase 1: add nullable FK columns ──────────────────────────────
        [
            migrations.AddField(
                model_name=name,
                name='workspace',
                field=models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                ),
            )
            for _, name in SCOPED_MODELS
        ]
        # ── Phase 2: stamp existing rows ──────────────────────────────────
        + [migrations.RunPython(stamp_default_workspace, noop)]
        # ── Phase 3: make NOT NULL ─────────────────────────────────────────
        + [
            migrations.AlterField(
                model_name=name,
                name='workspace',
                field=models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                ),
            )
            for _, name in SCOPED_MODELS
        ]
    )
