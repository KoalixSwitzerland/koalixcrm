# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.products.models.price import Price
from koalixcrm.reporting.models.resource import Resource


class ResourcePrice(Price):
    resource = models.ForeignKey(Resource,
                                 on_delete=models.CASCADE,
                                 verbose_name=_('Resource'),
                                 blank=False,
                                 null=False)

    def __str__(self):
        return str(self.price) + " " + str(self.currency.short_name)

    class Meta:
        app_label = "reporting"
        db_table = "crm_resourceprice"
