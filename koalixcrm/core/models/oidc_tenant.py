# -*- coding: utf-8 -*-
"""OidcTenant — a registered external IdP realm, keyed by its validated issuer.

koalixcrm#430. This model exists so that the ``<tenantAlias>`` segment of a
claim-derived group name (``oidc:<tenantAlias>:<claimValue>``, see
``koalixcrm/auth/oidc_backend.py``) has a source that is *server-side
configuration* rather than token content. An IdP can shape what a claim
says; it cannot create a row here.

Registering a row is therefore the deliberate per-issuer opt-in that
activates OIDC group synchronisation for that issuer. With no rows, the sync
is inert for every issuer — absence of a registration means "no eligible
``oidc:`` groups", never "any alias is acceptable".
"""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


class OidcTenant(models.Model):
    """A validated OIDC issuer mapped to the alias its groups are namespaced under."""

    alias = models.CharField(
        _('Alias'),
        max_length=100,
        unique=True,
        help_text=_(
            'Short identifier used verbatim as the <tenantAlias> segment of '
            'oidc:<tenantAlias>:<name> group names.'
        ),
    )
    issuer = models.CharField(
        _('Issuer'),
        max_length=255,
        unique=True,
        help_text=_('The validated OIDC issuer URL this tenant is derived from.'),
    )
    display_name = models.CharField(_('Display Name'), max_length=255, blank=True)

    class Meta:
        app_label = 'core'
        db_table = 'crm_oidctenant'
        verbose_name = _('OIDC Tenant')
        verbose_name_plural = _('OIDC Tenants')
        ordering = ['alias']

    def __str__(self) -> str:
        return self.display_name or self.alias
