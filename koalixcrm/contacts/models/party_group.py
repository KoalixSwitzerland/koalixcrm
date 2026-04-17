# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.const.party import PARTY_ROLE_CHOICES


class PartyGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    role_type_scope = models.CharField(
        max_length=32, choices=PARTY_ROLE_CHOICES,
        blank=True, null=True,
        verbose_name=_("Role type scope"),
        help_text=_("Optional — if set, membership is limited to parties playing this role."),
    )

    class Meta:
        app_label = "contacts"
        db_table = "crm_partygroup"
        verbose_name = _("Party group")
        verbose_name_plural = _("Party groups")

    def __str__(self):
        return self.name
