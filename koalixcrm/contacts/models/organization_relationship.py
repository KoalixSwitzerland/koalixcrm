# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.organization import Organization
from koalixcrm.core.const.party import ORG_RELATIONSHIP_CHOICES


class OrganizationRelationship(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name='child_relationships',
        verbose_name=_("Parent organization"),
    )
    child = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name='parent_relationships',
        verbose_name=_("Child organization"),
    )
    relationship_type = models.CharField(
        max_length=32, choices=ORG_RELATIONSHIP_CHOICES,
        verbose_name=_("Relationship type"),
    )
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contacts"
        db_table = "crm_organizationrelationship"
        verbose_name = _("Organization relationship")
        verbose_name_plural = _("Organization relationships")

    def __str__(self):
        return f"{self.parent_id}-{self.relationship_type}->{self.child_id}"
