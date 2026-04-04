# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.crm.contact.contact import Contact


class Supplier(Contact):
    offers_shipment_to_customers = models.BooleanField(verbose_name=_("Offers Shipment to Customer"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')

    def __str__(self):
        return str(self.id) + ' ' + self.name


