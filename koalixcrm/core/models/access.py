# -*- coding: utf-8 -*-
"""
Access-control models: Role enum, RoleInWorkspace.

CR-8 §8.2 – §8.3.  Object-level grants (RoleOnObject) are deferred to CR-10.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    ADMIN           = 'admin',           _('Admin (full control)')
    EDITOR          = 'editor',          _('Editor (edit + read)')
    VIEWER          = 'viewer',          _('Viewer (read only)')
    COMMENTER       = 'commenter',       _('Commenter (read + comment)')
    EMPLOYEE        = 'employee',        _('Employee (WFS: workflow participant)')
    LINE_MANAGER    = 'line_manager',    _('Line Manager (WFS: people management)')
    PROJECT_MANAGER = 'project_manager', _('Project Manager (WFS: project lead)')


class RoleInWorkspace(models.Model):
    """Workspace-level grant: which groups can access a workspace and at what role.

    Subject is a Django auth Group (not a User directly). Users gain access
    by membership in the group.

    CR-8 §8.3.
    """

    group = models.ForeignKey(
        'auth.Group',
        on_delete=models.CASCADE,
        related_name='workspace_roles',
        db_index=True,
        verbose_name=_('Group'),
        help_text=_('Django auth group whose members hold this role in the workspace'),
    )
    workspace = models.ForeignKey(
        'core.Workspace',
        on_delete=models.CASCADE,
        related_name='group_role_assignments',
        verbose_name=_('Workspace'),
    )
    role = models.CharField(
        max_length=64,
        choices=Role.choices,
        verbose_name=_('Role'),
    )

    def __str__(self):
        return f'{self.group.name} \u2192 {self.workspace.name} ({self.get_role_display()})'

    class Meta:
        app_label = 'core'
        db_table = 'crm_roleinworkspace'
        verbose_name = _('Role in Workspace')
        verbose_name_plural = _('Roles in Workspace')
        unique_together = [('group', 'workspace', 'role')]
