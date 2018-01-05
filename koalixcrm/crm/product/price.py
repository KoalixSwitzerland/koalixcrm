# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.product.currency import Currency
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.contact.customergroup import CustomerGroup


class CustomerGroupTransform(models.Model):
    from_customer_group = models.ForeignKey('CustomerGroup', verbose_name=_("From Unit"),
                                            related_name="db_reltransfromfromcustomergroup")
    to_customer_group = models.ForeignKey('CustomerGroup', verbose_name=_("To Unit"),
                                          related_name="db_reltransfromtocustomergroup")
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Customer Group"), blank=True, null=True)

    def transform(self, customer_group):
        if (self.from_customer_group == customer_group):
            return self.to_customer_group
        else:
            return unit

    def __str__(self):
        return "From " + self.from_customer_group.name + " to " + self.to_customer_group.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer Group Price Transfrom')
        verbose_name_plural = _('Customer Group Price Transfroms')


class Price(models.Model):
    product = models.ForeignKey("Product", verbose_name=_("Product"))
    unit = models.ForeignKey(Unit, blank=False, verbose_name=_("Unit"))
    currency = models.ForeignKey(Currency, blank=False, null=False, verbose_name=('Currency'))
    customer_group = models.ForeignKey(CustomerGroup, blank=True, null=True, verbose_name=_("Customer Group"))
    price = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Price Per Unit"))
    valid_from = models.DateField(verbose_name=_("Valid from"), blank=True, null=True)
    valid_until = models.DateField(verbose_name=_("Valid until"), blank=True, null=True)

    def is_valid_from_criteria_fulfilled(self, date):
        if self.valid_from == None:
            return True;
        elif (self.valid_from - date).days <= 0:
            return True;
        else:
            return False;

    def is_valid_until_criteria_fulfilled(self, date):
        if self.valid_until == None:
            return True
        elif (date - self.valid_until).days <= 0:
            return True
        else:
            return False

    def is_customer_group_criteria_fulfilled(self, customerGroup):
        if self.customer_group == None:
            return True
        elif self.customer_group == customerGroup:
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

    def matchesDateUnitCustomerGroupCurrency(self, date, unit, customer_group, currency):
        if (self.is_unit_criteria_fulfilled(unit) &
                self.is_currency_criteria_fulfilled(currency) &
                self.is_customer_group_criteria_fulfilled(customer_group) &
                self.is_valid_from_criteria_fulfilled(date) &
                self.is_valid_until_criteria_fulfilled(date)):
            return 1
        else:
            return 0

    class Meta:
        app_label = "crm"
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')


class ProductPrice(admin.TabularInline):
    model = Price
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('price', 'currency', 'unit', 'valid_from', 'valid_until', 'customer_group')
        }),
    )
    allow_add = True