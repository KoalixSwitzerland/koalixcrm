# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.party import Party
from koalixcrm.core.const.party import PARTY_ROLE_CHOICES
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class PartyRole(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    party = models.ForeignKey(
        Party, on_delete=models.CASCADE,
        related_name='roles',
        verbose_name=_("Party"),
    )
    role_type = models.CharField(
        max_length=32, choices=PARTY_ROLE_CHOICES,
        verbose_name=_("Role type"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contacts"
        db_table = "crm_partyrole"
        verbose_name = _("Party role")
        verbose_name_plural = _("Party roles")

    def __str__(self):
        return f"{self.party_id}:{self.role_type}"
