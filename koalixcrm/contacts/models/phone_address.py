# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _


class PhoneAddress(models.Model):
    phone = models.CharField(max_length=20,
                             verbose_name=_("Phone Number"))

    class Meta:
        app_label = "contacts"
        db_table = "crm_phoneaddress"
        verbose_name = _('Phone Address')
        verbose_name_plural = _('Phone Address')
