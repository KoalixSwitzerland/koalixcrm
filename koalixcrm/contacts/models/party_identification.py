# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.party import Party
from koalixcrm.core.const.party import IDENTIFICATION_SCHEME_CHOICES
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class PartyIdentification(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    party = models.ForeignKey(
        Party, on_delete=models.CASCADE,
        related_name='identifications',
        verbose_name=_("Party"),
    )
    scheme = models.CharField(
        max_length=16, choices=IDENTIFICATION_SCHEME_CHOICES,
        verbose_name=_("Scheme"),
    )
    value = models.CharField(max_length=128, verbose_name=_("Value"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contacts"
        db_table = "crm_partyidentification"
        verbose_name = _("Party identification")
        verbose_name_plural = _("Party identifications")

    def __str__(self):
        return f"{self.scheme}:{self.value}"
