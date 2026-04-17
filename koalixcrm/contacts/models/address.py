# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.const.country import COUNTRIES


class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    address_line_1 = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name=_("Address line 1"),
    )
    address_line_2 = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name=_("Address line 2"),
    )
    address_line_3 = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name=_("Address line 3"),
    )
    address_line_4 = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name=_("Address line 4"),
    )
    zip_code = models.CharField(
        max_length=16, blank=True, null=True,
        verbose_name=_("Zip code"),
    )
    town = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_("City"),
    )
    state = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_("State"),
    )
    country = models.CharField(
        max_length=2, choices=[(x[0], x[3]) for x in COUNTRIES],
        blank=True, null=True,
        verbose_name=_("Country"),
    )
    subdivision_code = models.CharField(
        max_length=3, blank=True, null=True,
        verbose_name=_("Subdivision code (ISO 3166-2 suffix)"),
    )

    class Meta:
        app_label = "contacts"
        db_table = "crm_address"
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        parts = [self.address_line_1, self.zip_code, self.town, self.country]
        return ' '.join(p for p in parts if p)
