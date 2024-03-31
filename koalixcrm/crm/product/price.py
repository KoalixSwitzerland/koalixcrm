# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.crm.product.currency import Currency
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.contact.customer_group import CustomerGroup
from koalixcrm.crm.product.unit_transform import UnitTransform
from koalixcrm.crm.product.customer_group_transform import CustomerGroupTransform
from koalixcrm.crm.product.currency_transform import CurrencyTransform


class Price(models.Model):
    id = models.BigAutoField(primary_key=True)
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             blank=False,
                             verbose_name=_("Unit"))
    currency = models.ForeignKey(Currency,
                                 on_delete=models.CASCADE,
                                 verbose_name='Currency',
                                 blank=False,
                                 null=False)
    customer_group = models.ForeignKey(CustomerGroup,
                                       on_delete=models.CASCADE,
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

    def __str__(self):
        return str(self.id) + " " +str(self.price) + " " + str(self.currency.short_name)

    def is_valid_from_criteria_fulfilled(self, date):
        if self.valid_from is None:
            return True
        elif (self.valid_from - date).days <= 0:
            return True
        else:
            return False

    def is_valid_until_criteria_fulfilled(self, date):
        if self.valid_until is None:
            return True
        elif (date - self.valid_until).days <= 0:
            return True
        else:
            return False

    def is_customer_group_criteria_fulfilled(self, customer_group):
        if self.customer_group is None:
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
        if (self.valid_from is None) and (self.valid_until is None):
            return True
        elif self.valid_until is None:
            if self.valid_from <= date:
                return True
            else:
                return False
        elif self.valid_from is None:
            if date <= self.valid_until:
                return True
            else:
                return False
        elif (self.valid_from <= date) and (date <= self.valid_until):
            return True
        else:
            return False

    def get_currency_transform_factor(self, currency, product_type):
        """check currency conditions and factor"""
        currency_factor = 0
        if self.currency == currency:
            currency_factor = 1
        else:
            currency_transform = CurrencyTransform.objects.get(from_currency=self.currency,
                                                               to_currency=currency,
                                                               product_type=product_type)
            if currency_transform:
                currency_factor = currency_transform.get_transform_factor()
        return currency_factor

    def get_unit_transform_factor(self, unit, product_type):
        """check unit conditions and factor"""
        unit_factor = 0
        if self.unit == unit:
            unit_factor = 1
        else:
            unit_transform = UnitTransform.objects.get(from_unit=self.unit,
                                                       to_unit=unit,
                                                       product_type=product_type)
            if unit_transform:
                unit_factor = unit_transform.get_transform_factor()
        return unit_factor

    def get_customer_group_transform_factor(self, customer, product_type):
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
        customer_group_factor = 0
        if self.customer_group is None:
            customer_group_factor = 1
        elif customer is not None:
            customer_groups = customer.is_member_of.all()
            if customer_groups is not None:
                for customer_group in customer_groups:
                    if self.customer_group == customer_group:
                        customer_group_factor = 1
                        # Stop for loop when a perfect match is found
                        break
                    else:
                        customer_group_transform = CustomerGroupTransform.objects.get(
                            from_customer_group=self.customer_group,
                            to_customer_group=customer_group,
                            product_type=product_type)
                        if customer_group_transform:
                            transform_factor = customer_group_transform.get_transform_factor()
                            if customer_group_factor > transform_factor or customer_group_factor == 0:
                                customer_group_factor = transform_factor
        return customer_group_factor

    class Meta:
        app_label = "crm"
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')
