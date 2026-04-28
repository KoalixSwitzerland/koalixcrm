# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.party import Party
from koalixcrm.core.const.country import COUNTRIES
from koalixcrm.core.const.party import LEGAL_FORM_CHOICES


class Organization(Party):
    legal_form = models.CharField(
        max_length=32, choices=LEGAL_FORM_CHOICES,
        blank=True, null=True,
        verbose_name=_("Legal form"),
    )
    legal_name = models.CharField(
        max_length=300, blank=True, null=True,
        verbose_name=_("Legal name"),
    )
    registration_number = models.CharField(
        max_length=64, blank=True, null=True,
        verbose_name=_("Registration number"),
    )
    legal_seat_country = models.CharField(
        max_length=2, choices=[(x[0], x[3]) for x in COUNTRIES],
        blank=True, null=True,
        verbose_name=_("Legal seat country"),
    )

    class Meta:
        app_label = "contacts"
        db_table = "crm_organization"
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
