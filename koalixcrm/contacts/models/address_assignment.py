# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.party import Party
from koalixcrm.contacts.models.address import Address
from koalixcrm.core.const.party import ASSIGNMENT_PURPOSE_CHOICES
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class AddressAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    party = models.ForeignKey(
        Party, on_delete=models.CASCADE,
        related_name='address_assignments',
        verbose_name=_("Party"),
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_("Address"),
    )
    purpose = models.CharField(
        max_length=16, choices=ASSIGNMENT_PURPOSE_CHOICES,
        verbose_name=_("Purpose"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contacts"
        db_table = "crm_addressassignment"
        verbose_name = _("Address assignment")
        verbose_name_plural = _("Address assignments")

    def __str__(self):
        return f"{self.party_id}-{self.purpose}-{self.address_id}"
