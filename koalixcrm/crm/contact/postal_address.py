# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.crm.const.country import *
from koalixcrm.crm.const.postaladdressprefix import *


class PostalAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    prefix = models.CharField(max_length=1,
                              choices=POSTALADDRESSPREFIX,
                              verbose_name=_("Prefix"), blank=True,
                              null=True)
    name = models.CharField(max_length=100,
                            verbose_name=_("Name"),
                            blank=True,
                            null=True)
    pre_name = models.CharField(max_length=100,
                                verbose_name=_("Pre-name"),
                                blank=True,
                                null=True)
    address_line_1 = models.CharField(max_length=200,
                                      verbose_name=_("Address line 1"),
                                      blank=True,
                                      null=True)
    address_line_2 = models.CharField(max_length=200,
                                      verbose_name=_("Address line 2"),
                                      blank=True,
                                      null=True)
    address_line_3 = models.CharField(max_length=200,
                                      verbose_name=_("Address line 3"),
                                      blank=True,
                                      null=True)
    address_line_4 = models.CharField(max_length=200,
                                      verbose_name=_("Address line 4"),
                                      blank=True,
                                      null=True)
    zip_code = models.IntegerField(verbose_name=_("Zip Code"),
                                   blank=True,
                                   null=True)
    town = models.CharField(max_length=100,
                            verbose_name=_("City"),
                            blank=True,
                            null=True)
    state = models.CharField(max_length=100,
                             verbose_name=_("State"),
                             blank=True,
                             null=True)
    country = models.CharField(max_length=2,
                               choices=[(x[0], x[3]) for x in COUNTRIES],
                               verbose_name=_("Country"),
                               blank=True,
                               null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address')
        verbose_name_plural = _('Postal Address')
