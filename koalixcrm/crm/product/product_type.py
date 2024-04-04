# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.crm.product.product_price import ProductPrice
from koalixcrm.crm.product.product_price import ProductPriceInlineAdminView
from koalixcrm.crm.product.unit_transform import UnitTransformInlineAdminView
from koalixcrm.crm.product.customer_group_transform import CustomerGroupTransformInlineAdminView
from koalixcrm.crm.product.currency_transform import CurrencyTransformInlineAdminView


class ProductType(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField(verbose_name=_("Description"),
                                   null=True,
                                   blank=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=200)
    product_type_identifier = models.CharField(verbose_name=_("Product Number"),
                                               max_length=200,
                                               null=True,
                                               blank=True)
    default_unit = models.ForeignKey("Unit", on_delete=models.CASCADE, verbose_name=_("Unit"))
    tax = models.ForeignKey("Tax",
                            on_delete=models.CASCADE,
                            blank=False,
                            null=False)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         null=True,
                                         blank=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    accounting_product_category = models.ForeignKey('accounting.ProductCategory',
                                                    on_delete=models.CASCADE,
                                                    verbose_name=_("Accounting Product Category"),
                                                    null=True,
                                                    blank=True)

    def get_price(self, date, unit, customer, currency):
        """The function searches for a valid price and returns the price of the product as a decimal value.

        Args:
            koalixcrm.crm.contact.customer customer
            koalixcrm.crm.product.unit unit
            koalixcrm.crm.product.currency currency
            datetime.date date

        Returns:
            when a match is found: dict customer_group_factors name=customer_group, value=factor
            when no match is found: customer_group_factors is None

        Raises:
            In case the algorithm does not find a valid product price, the function raises a
            NoPriceFound Exception"""
        prices = ProductPrice.objects.filter(product_type=self)
        valid_prices = list()
        for price in list(prices):
            currency_factor = price.get_currency_transform_factor(currency, self.id)
            unit_factor = price.get_unit_transform_factor(unit, self.id)
            group_factor = price.get_customer_group_transform_factor(customer, self.id)
            date_in_range = price.is_date_in_range(date)
            if date_in_range \
                    and currency_factor != 0 \
                    and unit_factor != 0 \
                    and group_factor != 0:
                transformed_price = price.price*group_factor*unit_factor*currency_factor
                valid_prices.append(transformed_price)
        if len(valid_prices) > 0:
            lowest_price = valid_prices[0]
            for price in valid_prices:
                if price < lowest_price:
                    lowest_price = price
            return lowest_price
        else:
            raise ProductType.NoPriceFound(customer, unit, date, currency, self)

    def get_tax_rate(self):
        return self.tax.get_tax_rate()

    def __str__(self):
        return str(self.product_type_identifier) + ' ' + self.title.__str__()

    class Meta:
        app_label = "crm"
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')

    class NoPriceFound(Exception):
        def __init__(self, customer, unit, date, currency, product):
            self.customer = customer
            self.unit = unit
            self.date = date
            self.product = product
            self.currency = currency
            return

        def __str__(self):
            return _("There is no Price for this product type") + ": " + self.product.__str__() + _(
                "that matches the date") + ": " + self.date.__str__() + " ," + _(
                "customer") + ": " + self.customer.__str__() + " ," + _(
                "currency") + ": " + self.currency.__str__() + _(" and unit") + ":" + self.unit.__str__()


class ProductTypeAdminView(admin.ModelAdmin):
    list_display = (
        'product_type_identifier',
        'title',
        'default_unit',
        'tax',
        'accounting_product_category')
    list_display_links = ('product_type_identifier',)
    fieldsets = (
        (_('Basics'), {
            'fields': (
                'product_type_identifier',
                'title',
                'description',
                'default_unit',
                'tax',
                'accounting_product_category')
        }),
    )
    inlines = [ProductPriceInlineAdminView,
               UnitTransformInlineAdminView,
               CurrencyTransformInlineAdminView,
               CustomerGroupTransformInlineAdminView]
