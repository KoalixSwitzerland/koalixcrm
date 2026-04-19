# -*- coding: utf-8 -*-
# Generated migration for CR-8: Workspace, RoleInWorkspace, WorkspaceSwitchEvent.
# RoleOnObject deferred to CR-10 (object-level grants).
#
# Schema-only — no data migration.  The Default Workspace data migration
# lives in CR-9 (CR §8.8).

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from koalixcrm.migration_utils import CreateModelIfNotExists


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_pdf_export_process'),
        ('contacts', '0010_drop_partycontact_preferred_language'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 1. Workspace --------------------------------------------------------
        CreateModelIfNotExists(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
                ('color', models.CharField(
                    blank=True, max_length=7,
                    help_text='Hex color used by the admin header as a visual cue to prevent workspace mix-ups.',
                    verbose_name='Color',
                )),
                ('description', models.TextField(
                    blank=True,
                    default='',
                    verbose_name='Description',
                )),
                ('external_workspace_reference', models.CharField(
                    blank=True,
                    default='',
                    max_length=255,
                    verbose_name='External Workspace Reference',
                    help_text='Short prefix for human-readable identifiers (e.g. REP, MSD). Used in IDs like REP-TASK-1.',
                )),
                ('is_active', models.BooleanField(
                    default=True,
                    db_index=True,
                    verbose_name='Is Active',
                )),
                ('date_added', models.DateField(auto_now_add=True, verbose_name='Date Added')),
                ('last_modified', models.DateField(auto_now=True, verbose_name='Last Modified')),
                ('organization', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='workspaces',
                    to='contacts.organization',
                    help_text='Optional: the legal entity this workspace represents.',
                    verbose_name='Organization',
                )),
            ],
            options={
                'verbose_name': 'Workspace',
                'verbose_name_plural': 'Workspaces',
                'db_table': 'crm_workspace',
                'ordering': ['name'],
                'app_label': 'core',
            },
        ),

        # 2. RoleInWorkspace --------------------------------------------------
        CreateModelIfNotExists(
            name='RoleInWorkspace',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(
                    max_length=64,
                    choices=[
                        ('admin',           'Admin (full control)'),
                        ('editor',          'Editor (edit + read)'),
                        ('viewer',          'Viewer (read only)'),
                        ('commenter',       'Commenter (read + comment)'),
                        ('employee',        'Employee (WFS: workflow participant)'),
                        ('line_manager',    'Line Manager (WFS: people management)'),
                        ('project_manager', 'Project Manager (WFS: project lead)'),
                    ],
                    verbose_name='Role',
                )),
                ('group', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='workspace_roles',
                    to='auth.group',
                    db_index=True,
                    verbose_name='Group',
                    help_text='Django auth group whose members hold this role in the workspace',
                )),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='group_role_assignments',
                    to='core.workspace',
                    verbose_name='Workspace',
                )),
            ],
            options={
                'verbose_name': 'Role in Workspace',
                'verbose_name_plural': 'Roles in Workspace',
                'db_table': 'crm_roleinworkspace',
                'unique_together': {('group', 'workspace', 'role')},
                'indexes': [
                    models.Index(fields=['group', 'workspace'], name='crm_riw_group_ws_idx'),
                ],
                'app_label': 'core',
            },
        ),

        # 3. WorkspaceSwitchEvent ---------------------------------------------
        CreateModelIfNotExists(
            name='WorkspaceSwitchEvent',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('from_workspace', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='+',
                    to='core.workspace',
                    verbose_name='From Workspace',
                )),
                ('to_workspace', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='+',
                    to='core.workspace',
                    verbose_name='To Workspace',
                )),
                ('user', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='+',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='User',
                )),
            ],
            options={
                'verbose_name': 'Workspace Switch Event',
                'verbose_name_plural': 'Workspace Switch Events',
                'db_table': 'crm_workspaceswitchevent',
                'ordering': ['-timestamp'],
                'indexes': [
                    models.Index(fields=['user', 'timestamp'], name='crm_wsswevent_user_ts_idx'),
                ],
                'app_label': 'core',
            },
        ),
    ]
