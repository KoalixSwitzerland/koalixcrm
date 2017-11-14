# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.product.currency import Currency
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.contact.customergroup import CustomerGroup

import koalixcrm.crm.product.product


class CustomerGroupTransform(models.Model):
    fromCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name=_("From Unit"),
                                          related_name="db_reltransfromfromcustomergroup")
    toCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name=_("To Unit"),
                                        related_name="db_reltransfromtocustomergroup")
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Customer Group"), blank=True, null=True)

    def transform(self, customerGroup):
        if (self.fromCustomerGroup == customerGroup):
            return self.toCustomerGroup
        else:
            return unit

    def __str__(self):
        return "From " + self.fromCustomerGroup.name + " to " + self.toCustomerGroup.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer Group Price Transfrom')
        verbose_name_plural = _('Customer Group Price Transfroms')


class Price(models.Model):
    product = models.ForeignKey("Product", verbose_name=_("Product"))
    unit = models.ForeignKey(Unit, blank=False, verbose_name=_("Unit"))
    currency = models.ForeignKey(Currency, blank=False, null=False, verbose_name=('Currency'))
    customerGroup = models.ForeignKey(CustomerGroup, blank=True, null=True, verbose_name=_("Customer Group"))
    price = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Price Per Unit"))
    validfrom = models.DateField(verbose_name=_("Valid from"), blank=True, null=True)
    validuntil = models.DateField(verbose_name=_("Valid until"), blank=True, null=True)

    def is_valid_from_criteria_fulfilled(self, date):
        if self.validfrom == None:
            return True;
        elif (self.validfrom - date).days <= 0:
            return True;
        else:
            return False;

    def is_valid_until_criteria_fulfilled(self, date):
        if self.validuntil == None:
            return True
        elif (date - self.validuntil).days <= 0:
            return True
        else:
            return False

    def is_customer_group_criteria_fulfilled(self, customerGroup):
        if self.customerGroup == None:
            return True
        elif self.customerGroup == customerGroup:
            return True
        else:
            return False

    def is_currency_criteria_fulfilled(self, currency):
        if self.currency == currency:
            return True
        else:
            return False

    def is_unit_criteria_fulfilled(self, unit):
        if self.unit == unit:
            return True
        else:
            return False

    def matchesDateUnitCustomerGroupCurrency(self, date, unit, customerGroup, currency):
        if (self.is_unit_criteria_fulfilled(unit) &
                self.is_currency_criteria_fulfilled(currency) &
                self.is_customer_group_criteria_fulfilled(customerGroup) &
                self.is_valid_from_criteria_fulfilled(date) &
                self.is_valid_until_criteria_fulfilled(date)):
            return 1
        else:
            return 0

    class Meta:
        app_label = "crm"
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

