# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.country import *
from koalixcrm.crm.const.postaladdressprefix import *


class PostalAddress(models.Model):
    prefix = models.CharField(max_length=1, choices=POSTALADDRESSPREFIX, verbose_name=_("Prefix"), blank=True,
                              null=True)
    name = models.CharField(max_length=100, verbose_name=_("Name"), blank=True, null=True)
    prename = models.CharField(max_length=100, verbose_name=_("Prename"), blank=True, null=True)
    addressline1 = models.CharField(max_length=200, verbose_name=_("Addressline 1"), blank=True, null=True)
    addressline2 = models.CharField(max_length=200, verbose_name=_("Addressline 2"), blank=True, null=True)
    addressline3 = models.CharField(max_length=200, verbose_name=_("Addressline 3"), blank=True, null=True)
    addressline4 = models.CharField(max_length=200, verbose_name=_("Addressline 4"), blank=True, null=True)
    zipcode = models.IntegerField(verbose_name=_("Zipcode"), blank=True, null=True)
    town = models.CharField(max_length=100, verbose_name=_("City"), blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name=_("State"), blank=True, null=True)
    country = models.CharField(max_length=2, choices=[(x[0], x[3]) for x in COUNTRIES], verbose_name=_("Country"),
                               blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address')
        verbose_name_plural = _('Postal Address')