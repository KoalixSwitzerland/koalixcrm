# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


# Class is named `PartyEmail` (not `EmailAddress`) to avoid colliding with the
# legacy `koalixcrm.contacts.models.email_address.EmailAddress` during the
# #392..#394 coexistence phase. Renamed to `EmailAddress` in #395.
class PartyEmail(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=200, verbose_name=_("Email"))

    class Meta:
        app_label = "contacts"
        db_table = "crm_partyemail"
        verbose_name = _("Email address")
        verbose_name_plural = _("Email addresses")

    def __str__(self) -> str:
        return self.email
