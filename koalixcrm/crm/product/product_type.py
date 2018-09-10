# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext as _

from koalixcrm.crm.product.price import Price
from koalixcrm.crm.product.price import ProductPrice
from koalixcrm.crm.product.unit_transform import ProductUnitTransform
from koalixcrm.crm.product.customer_group_transform import ProductCustomerGroupTransform
from koalixcrm.crm.product.currency_transform import ProductCurrencyTransform


class ProductType(models.Model):
    description = models.TextField(verbose_name=_("Description"),
                                   null=True,
                                   blank=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=200)
    product_identifier = models.CharField(verbose_name=_("Product Number"),
                                          max_lenghth=200,
                                          null=True,
                                          blank=True)
    default_unit = models.ForeignKey("Unit", verbose_name=_("Unit"))
    tax = models.ForeignKey("Tax",
                            blank=False,
                            null=False)
    product_category = models.ForeignKey("ProductCategory",
                                         blank=False,
                                         null=False)
    product_status = models.ForeignKey("ProductStatus",
                                       blank=False,
                                       null=False)
    last_status_change = models.DateField(verbose_name=_("Last Status Change"),
                                          blank=True,
                                          null=False)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         null=True,
                                         blank=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    accounting_product_categorie = models.ForeignKey('accounting.ProductCategorie',
                                                     verbose_name=_("Accounting Product Categorie"),
                                                     null=True,
                                                     blank="True")

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
        prices = Price.objects.filter(product_type=self.id)
        valid_prices = list()
        for price in list(prices):
            currency_factor = price.get_currency_transform_factor(price)
            unit_factor = price.get_unit_transform_factor(price)
            group_factors = price.get_customer_group_transform_factor(customer)
            date_in_range = price.is_date_in_range(date)
            if currency_factor != 0 and \
                    group_factors != 0 and \
                    date_in_range and \
                    unit_factor != 0:

                transformed_price = price.price*group_factors*unit_factor*unit_factor
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
        return str(self.product_identifier) + ' ' + self.title.__str__()

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


class OptionProductType(admin.ModelAdmin):
    list_display = ('product_type_number',
                    'title',
                    'default_unit',
                    'tax',
                    'accounting_product_categorie')
    list_display_links = ('product_number',)
    fieldsets = (
        (_('Basics'), {
                       'title',
                       'description',
                       'default_unit',
                       'tax',
                       'accounting_product_categorie'
        }),)
    inlines = [ProductPrice,
               ProductUnitTransform,
               ProductCurrencyTransform,
               ProductCustomerGroupTransform]
