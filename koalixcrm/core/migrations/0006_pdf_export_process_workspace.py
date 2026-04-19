# -*- coding: utf-8 -*-
"""
CR-9 migration: add workspace FK to PDFExportProcess.

Phase 1: AddField nullable.
Phase 2: Data migration — get-or-create Default Workspace, stamp existing rows.
Phase 3: AlterField to NOT NULL.
"""

import django.db.models.deletion
from django.db import migrations, models

from koalixcrm.migration_utils import AddFieldIfNotExists


def stamp_default_workspace(apps, schema_editor):
    Workspace = apps.get_model('core', 'Workspace')
    PDFExportProcess = apps.get_model('core', 'PDFExportProcess')

    ws, _ = Workspace.objects.get_or_create(
        name='Default Workspace',
        defaults={'is_active': True},
    )
    PDFExportProcess.objects.filter(workspace__isnull=True).update(workspace=ws)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_workspace_and_access'),
    ]

    operations = [
        # Phase 1: nullable FK
        AddFieldIfNotExists(
            model_name='pdfexportprocess',
            name='workspace',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
                verbose_name='Workspace',
            ),
            preserve_default=False,
        ),

        # Phase 2: data migration
        migrations.RunPython(stamp_default_workspace, reverse_code=noop),

        # Phase 3: make NOT NULL
        migrations.AlterField(
            model_name='pdfexportprocess',
            name='workspace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='core.workspace',
                verbose_name='Workspace',
            ),
        ),
    ]
