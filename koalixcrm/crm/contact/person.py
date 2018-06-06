# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.postaladdressprefix import *


class Person(models.Model):
    prefix = models.CharField(max_length=1,
                              choices=POSTALADDRESSPREFIX,
                              verbose_name=_("Prefix"),
                              blank=True,
                              null=True)
    name = models.CharField(max_length=100, verbose_name=_("Name"), blank=True, null=True)
    prename = models.CharField(max_length=100, verbose_name=_("Prename"), blank=True, null=True)
    email = models.EmailField(max_length=200, verbose_name=_("Email Address"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    role = models.CharField(max_length=100, verbose_name=_("Role"), blank=True, null=True)
    companies = models.ManyToManyField("Contact",
                                       through='ContactPersonAssociation',
                                       verbose_name=_('Works at'), blank=True)

    def __str__(self):
        return self.prename + ' ' + self.name + ' - ' + self.email
    
    class Meta:
        app_label = "crm"
        verbose_name = _('Person')
        verbose_name_plural = _('People')
