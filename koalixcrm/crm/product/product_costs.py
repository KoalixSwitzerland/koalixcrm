# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.product.currency import Currency
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.contact.customer_group import CustomerGroup
from koalixcrm.crm.product.unit_transform import UnitTransform
from koalixcrm.crm.product.customer_group_transform import CustomerGroupTransform
from koalixcrm.crm.product.currency_transform import CurrencyTransform


class Cost(models.Model):
    product = models.ForeignKey("Product",
                                verbose_name=_("Product"))
    unit = models.ForeignKey(Unit,
                             blank=False,
                             verbose_name=_("Unit"))
    currency = models.ForeignKey(Currency,
                                 verbose_name='Currency',
                                 blank=False,
                                 null=False)
    customer_group = models.ForeignKey(CustomerGroup,
                                       verbose_name=_("Customer Group"),
                                       blank=True,
                                       null=True)
    cost = models.DecimalField(max_digits=17,
                               decimal_places=2,
                               verbose_name=_("Cost Per Unit"))
    date = models.DateField(verbose_name=_("Cost date"),
                            blank=True,
                            null=True)
