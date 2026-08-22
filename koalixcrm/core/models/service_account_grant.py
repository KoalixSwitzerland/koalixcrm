# -*- coding: utf-8 -*-
"""ServiceAccountGrant — marks a Django user as an unrestricted service account.

koalixcrm#432. Core-owned and deliberately free of business semantics: the
mere existence of a row for a user is the entire signal
``koalixcrm.core.access.is_unrestricted_actor`` reads.

The point of a dedicated model is that the signal conferring the system's
widest authority stops being a *string comparison against a group name* in a
system where group names are partly externally sourced (see
``koalixcrm/auth/oidc_backend.py``). ``settings.M2M_MICROSERVICE_GROUP_NAME``
may keep carrying Django model permissions for the permission-based modules,
but it no longer answers "is this the service account".

Rows are written administratively — through the superuser-only admin or the
``grant_service_account`` management command — and **never** by an
authentication or synchronisation code path, so that being able to obtain a
token is never sufficient to become the service account.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ServiceAccountGrant(models.Model):
    """A row for ``user`` marks that user as an unrestricted service account.

    ``OneToOneField`` both expresses and enforces "at most one grant per
    user" — a second attempt for the same user fails at the database level,
    on top of whatever application-level idempotency a caller provides.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_account_grant',
        verbose_name=_('User'),
        help_text=_('The Django user this grant marks as an unrestricted service account.'),
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        app_label = 'core'
        db_table = 'crm_serviceaccountgrant'
        verbose_name = _('Service Account Grant')
        verbose_name_plural = _('Service Account Grants')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'ServiceAccountGrant(user={self.user_id})'
