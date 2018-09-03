# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext as _

from koalixcrm.crm.product.price import Price
from koalixcrm.crm.product.price import ProductPrice
from koalixcrm.crm.product.unit_transform import ProductUnitTransform
from koalixcrm.crm.product.customer_group_transform import ProductCustomerGroupTransform
from koalixcrm.crm.product.currency_transform import ProductCurrencyTransform


class Product(models.Model):
    description = models.TextField(verbose_name=_("Description"),
                                   null=True,
                                   blank=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=200)
    product_number = models.IntegerField(verbose_name=_("Product Number"))
    default_unit = models.ForeignKey("Unit", verbose_name=_("Unit"))
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         null=True,
                                         blank="True")
    tax = models.ForeignKey("Tax",
                            blank=False)
    accounting_product_categorie = models.ForeignKey('accounting.ProductCategorie',
                                                     verbose_name=_("Accounting Product Categorie"),
                                                     null=True,
                                                     blank="True")

    def get_price(self, date, unit, customer, currency):
        prices = Price.objects.filter(product=self.id)
        valid_prices = list()
        for price in list(prices):
            currency_factor = price.get_currency_transform_factor(price)
            unit_factor = price.get_unit_transform_factor(price)
            group_factor = price.get_customer_group_transform_factor(customer)
            if currency_factor != 0 and \
                    group_factor != 0 and \
                    unit_factor != 0:
                valid_prices.append(price)
        if len(valid_prices) > 0:
            lowest_price = valid_prices[0]
            for price in valid_prices:
                if price < lowest_price:
                    lowest_price = price
            return lowest_price
        else:
            raise Product.NoPriceFound(customer, unit, date, currency, self)

    def get_tax_rate(self):
        return self.tax.get_tax_rate()

    def __str__(self):
        return str(self.product_number) + ' ' + self.title.__str__()

    class Meta:
        app_label = "crm"
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    class NoPriceFound(Exception):
        def __init__(self, customer, unit, date, currency, product):
            self.customer = customer
            self.unit = unit
            self.date = date
            self.product = product
            self.currency = currency
            return

        def __str__(self):
            return _("There is no Price for this product") + ": " + self.product.__str__() + _(
                "that matches the date") + ": " + self.date.__str__() + " ," + _(
                "customer") + ": " + self.customer.__str__() + " ," + _(
                "currency") + ": " + self.currency.__str__() + _(" and unit") + ":" + self.unit.__str__()


class OptionProduct(admin.ModelAdmin):
    list_display = ('product_number',
                    'title',
                    'default_unit',
                    'tax',
                    'accounting_product_categorie')
    list_display_links = ('product_number',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('product_number',
                       'title',
                       'description',
                       'default_unit',
                       'tax',
                       'accounting_product_categorie')
        }),)
    inlines = [ProductPrice,
               ProductUnitTransform,
               ProductCurrencyTransform,
               ProductCustomerGroupTransform]
