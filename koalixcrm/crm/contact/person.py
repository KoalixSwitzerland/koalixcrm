# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.crm.const.postaladdressprefix import *


class Person(models.Model):
    id = models.BigAutoField(primary_key=True)
    prefix = models.CharField(max_length=1,
                              choices=POSTALADDRESSPREFIX,
                              verbose_name=_("Prefix"),
                              blank=True,
                              null=True)
    name = models.CharField(max_length=100,
                            verbose_name=_("Name"),
                            blank=True,
                            null=True)
    pre_name = models.CharField(max_length=100,
                                verbose_name=_("Pre-name"),
                                blank=True,
                                null=True)
    email = models.EmailField(max_length=200,
                              verbose_name=_("Email Address"))
    phone = models.CharField(max_length=20,
                             verbose_name=_("Phone Number"))
    role = models.CharField(max_length=100,
                            verbose_name=_("Role"),
                            blank=True,
                            null=True)
    companies = models.ManyToManyField("Contact",
                                       through='ContactPersonAssociation',
                                       verbose_name=_('Works at'), blank=True)

    def get_pre_name(self):
        if self.pre_name:
            return self.pre_name
        else:
            return "n/a"

    def get_name(self):
        if self.name:
            return self.name
        else:
            return "n/a"

    def get_email(self):
        if self.email:
            return self.email
        else:
            return "n/a"

    def __str__(self):
        return self.get_pre_name() + ' ' + self.get_name() + ' - ' + self.get_email()
    
    class Meta:
        app_label = "crm"
        verbose_name = _('Person')
        verbose_name_plural = _('People')
