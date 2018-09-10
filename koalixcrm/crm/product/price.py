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


class Price(models.Model):
    product_type = models.ForeignKey("Product Type",
                                     verbose_name=_("Product Type"))
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
    price = models.DecimalField(max_digits=17,
                                decimal_places=2,
                                verbose_name=_("Price Per Unit"))
    valid_from = models.DateField(verbose_name=_("Valid from"),
                                  blank=True,
                                  null=True)
    valid_until = models.DateField(verbose_name=_("Valid until"),
                                   blank=True,
                                   null=True)

    def is_valid_from_criteria_fulfilled(self, date):
        if not self.valid_from:
            return True
        elif (self.valid_from - date).days <= 0:
            return True
        else:
            return False

    def is_valid_until_criteria_fulfilled(self, date):
        if not self.valid_until:
            return True
        elif (date - self.valid_until).days <= 0:
            return True
        else:
            return False

    def is_customer_group_criteria_fulfilled(self, customer_group):
        if not self.customer_group:
            return True
        elif self.customer_group == customer_group:
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

    def is_date_in_range(self, date):
        if (self.valid_from <= date) and (date <= self.valid_until):
            return True
        else:
            return False

    def get_currency_transform_factor(self, currency, product):
        """check currency conditions and factor"""
        if self.currency == currency:
            currency_factor = 1
        else:
            currency_transform = CurrencyTransform.objects.get(from_currency=self.currency,
                                                               to_currency=currency,
                                                               product=product)
            if currency_transform:
                currency_transform.get_transfrom_factor()
            else:
                currency_factor = 0
        return currency_factor

    def get_unit_transform_factor(self, unit, product):
        """check unit conditions and factor"""
        if self.unit == unit:
            unit_factor = 1
        else:
            unit_transform = UnitTransform.objects.get(from_unit=self.unit,
                                                       to_unit=unit,
                                                       product=product)
            if unit_transform:
                unit_transform.get_transfrom_factor()
            else:
                unit_factor = 0
        return unit_factor

    def get_customer_group_transform_factor(self, customer, product):
        """The function searches through all customer_groups in which the customer is member of
        from these customer_groups, the function returns the customer_group with the perfect match
        or it returns the factor with the lowest transform factor

        Args:
            koalixcrm.crm.contact.customer customer
            koalixcrm.crm.product.product product

        Returns:
            Decimal factor

        Raises:
            No exceptions planned"""
        customer_groups = CustomerGroup.objects.filter(customer=customer)
        customer_group_factor = 0
        for customer_group in customer_groups:
            if self.customer_group == customer_group:
                customer_group_factor = 1
                """Stop for loop when a perfect match is found"""
                break
            else:
                customer_group = CustomerGroupTransform.objects.get(from_customer_group=self.customer_group,
                                                                    to_customer_group=customer_group,
                                                                    product=product)
                if customer_group:
                    if customer_group_factor > customer_group.get_transfrom_factor():
                        customer_group_factor = customer_group.get_transfrom_factor()
        return customer_group_factor

    def matches_date_unit_customer_group_currency(self, date, unit, customer_group, currency):
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
            'fields': ('price',
                       'currency',
                       'unit',
                       'valid_from',
                       'valid_until',
                       'customer_group')
        }),
    )
    allow_add = True
