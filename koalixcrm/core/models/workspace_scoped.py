# -*- coding: utf-8 -*-
"""
WorkspaceScopedModel — abstract base for all tenant-scoped models.

CR-9 §9.1.
"""

from django.db import models

from koalixcrm.core.managers.workspace_aware import WorkspaceAwareManager


class WorkspaceScopedModel(models.Model):
    workspace = models.ForeignKey(
        'core.Workspace',
        on_delete=models.CASCADE,
        related_name='+',
    )

    objects = WorkspaceAwareManager()

    class Meta:
        abstract = True
