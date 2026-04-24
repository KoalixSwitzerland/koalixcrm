# -*- coding: utf-8 -*-
"""
Workspace model — the tenant (coarse scope) shared between koalixcrm and WFS.

CR-8 §8.1.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Workspace(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Name'),
    )
    organization = models.ForeignKey(
        'contacts.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workspaces',
        help_text=_('Optional: the legal entity this workspace represents.'),
        verbose_name=_('Organization'),
    )
    color = models.CharField(
        max_length=7,
        blank=True,
        help_text=_('Hex color used by the admin header as a visual cue to prevent workspace mix-ups.'),
        verbose_name=_('Color'),
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name=_('Description'),
    )
    external_workspace_reference = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('External Workspace Reference'),
        help_text=_('Short prefix for human-readable identifiers (e.g. REP, MSD). Used in IDs like REP-TASK-1.'),
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_('Is Active'),
    )
    date_added = models.DateField(auto_now_add=True, verbose_name=_('Date Added'))
    last_modified = models.DateField(auto_now=True, verbose_name=_('Last Modified'))

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'core'
        db_table = 'crm_workspace'
        verbose_name = _('Workspace')
        verbose_name_plural = _('Workspaces')
        ordering = ['name']
