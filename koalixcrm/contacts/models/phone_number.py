# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _


class PhoneNumber(models.Model):
    id = models.BigAutoField(primary_key=True)
    phone_e164 = models.CharField(max_length=32, verbose_name=_("Phone (E.164)"))

    class Meta:
        app_label = "contacts"
        db_table = "crm_phonenumber"
        verbose_name = _("Phone number")
        verbose_name_plural = _("Phone numbers")

    def __str__(self):
        return self.phone_e164
