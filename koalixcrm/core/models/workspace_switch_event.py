# -*- coding: utf-8 -*-
"""
WorkspaceSwitchEvent — audit row written every time a user switches their
active workspace via the dashboard module or the header switcher.

CR-8 §8.6.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkspaceSwitchEvent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',
        verbose_name=_('User'),
    )
    from_workspace = models.ForeignKey(
        'core.Workspace',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_('From Workspace'),
    )
    to_workspace = models.ForeignKey(
        'core.Workspace',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',
        verbose_name=_('To Workspace'),
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))

    def __str__(self) -> str:
        return f'{self.user}: {self.from_workspace} → {self.to_workspace} at {self.timestamp}'

    class Meta:
        app_label = 'core'
        db_table = 'crm_workspaceswitchevent'
        verbose_name = _('Workspace Switch Event')
        verbose_name_plural = _('Workspace Switch Events')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]
