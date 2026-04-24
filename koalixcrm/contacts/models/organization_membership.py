# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.organization import Organization
from koalixcrm.contacts.models.natural_person import PartyContact
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class OrganizationMembership(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    contact = models.ForeignKey(
        PartyContact, on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name=_("Contact"),
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_("Organization"),
    )
    title = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_("Title"),
    )
    position = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_("Position"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contacts"
        db_table = "crm_organizationmembership"
        verbose_name = _("Organization membership")
        verbose_name_plural = _("Organization memberships")

    def __str__(self):
        return f"{self.contact_id}@{self.organization_id}"
