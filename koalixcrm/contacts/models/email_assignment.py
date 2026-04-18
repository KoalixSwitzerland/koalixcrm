# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.party import Party
from koalixcrm.contacts.models.party_email import PartyEmail
from koalixcrm.core.const.party import ASSIGNMENT_PURPOSE_CHOICES


class EmailAssignment(models.Model):
    id = models.BigAutoField(primary_key=True)
    party = models.ForeignKey(
        Party, on_delete=models.CASCADE,
        related_name='email_assignments',
        verbose_name=_("Party"),
    )
    email = models.ForeignKey(
        PartyEmail, on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_("Email"),
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
        db_table = "crm_emailassignment"
        verbose_name = _("Email assignment")
        verbose_name_plural = _("Email assignments")

    def __str__(self):
        return f"{self.party_id}-{self.purpose}-{self.email_id}"
