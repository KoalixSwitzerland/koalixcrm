# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.contact.contact import Contact


class Supplier(Contact):
    offersShipmentToCustomers = models.BooleanField(verbose_name=_("Offers Shipment to Customer"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Supplier')
        verbose_name_plural = _('Supplier')

    def __str__(self):
        return str(self.id) + ' ' + self.name

