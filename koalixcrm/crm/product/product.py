# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.accounting.models import ProductCategorie
from rest_framework import serializers

import koalixcrm.crm.product.price
from koalixcrm.accounting.accounting.product_categorie import ProductCategoryMinimalJSONSerializer
from koalixcrm.crm.contact.customergroup import CustomerGroup
from koalixcrm.crm.product.price import ProductPrice
from koalixcrm.crm.product.tax import Tax, TaxMinimalJSONSerializer
from koalixcrm.crm.product.unit import ProductUnitTransform
from koalixcrm.crm.product.unit import UnitTransform, Unit, UnitMinimalJSONSerializer


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
        prices = koalixcrm.crm.product.price.Price.objects.filter(product=self.id)
        unit_transforms = UnitTransform.objects.filter(product=self.id)
        customer_group_transforms = koalixcrm.crm.product.price.CustomerGroupTransform.objects.filter(product=self.id)
        valid_prices = list()
        for price in list(prices):
            for customerGroup in CustomerGroup.objects.filter(customer=customer):
                if price.matchesDateUnitCustomerGroupCurrency(date, unit, customerGroup, currency):
                    valid_prices.append(price.price)
                else:
                    for customerGroupTransform in customer_group_transforms:
                        if price.matchesDateUnitCustomerGroupCurrency(date,
                                                                      unit,
                                                                      customerGroupTransform.transform(customerGroup),
                                                                      currency):
                            valid_prices.append(price.price * customerGroup.factor);
                        else:
                            for unitTransform in list(unit_transforms):
                                if price.matchesDateUnitCustomerGroupCurrency(date,
                                                                              unitTransform.transfrom(unit).transform(
                                                                                  unitTransform),
                                                                              customerGroupTransform.transform(
                                                                                  customerGroup), currency):
                                    valid_prices.append(
                                        price.price * customerGroupTransform.factor * unitTransform.factor);
        if len(valid_prices) > 0:
            lowest_price = valid_prices[0]
            for price in valid_prices:
                if price < lowest_price:
                    lowest_price = price
            return lowest_price
        else:
            raise Product.NoPriceFound(customer, unit, date, currency, self)

    def get_tax_rate(self):
        return self.tax.get_tax_rate();

    def __str__(self):
        return str(self.product_number) + ' ' + self.title

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
    list_display = ('product_number', 'title', 'default_unit', 'tax', 'accounting_product_categorie')
    list_display_links = ('product_number',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('product_number', 'title', 'description', 'default_unit', 'tax', 'accounting_product_categorie')
        }),)
    inlines = [ProductPrice, ProductUnitTransform]


class ProductJSONSerializer(serializers.HyperlinkedModelSerializer):
    productNumber = serializers.IntegerField(source='product_number',
                                             allow_null=False)
    unit = UnitMinimalJSONSerializer(source='default_unit',
                                     allow_null=False)
    tax = TaxMinimalJSONSerializer(allow_null=False)
    productCategory = ProductCategoryMinimalJSONSerializer(source='accounting_product_categorie',
                                                           allow_null=False)

    class Meta:
        model = Product
        fields = ('id',
                  'productNumber',
                  'title',
                  'unit',
                  'tax',
                  'productCategory')
        depth = 1

    def create(self, validated_data):
        product = Product()
        product.product_number = validated_data['product_number']
        product.title = validated_data['title']

        # Deserialize default_unit
        default_unit = validated_data.pop('default_unit')
        if default_unit:
            if default_unit.get('id', None):
                product.default_unit = Unit.objects.get(id=default_unit.get('id', None))
            else:
                product.default_unit = None

        # Deserialize tax
        tax = validated_data.pop('tax')
        if tax:
            if tax.get('id', None):
                product.tax = Tax.objects.get(id=tax.get('id', None))
            else:
                product.tax = None

        # Deserialize product category
        product_category = validated_data.pop('accounting_product_categorie')
        if product_category:
            if product_category.get('id', None):
                product.accounting_product_categorie = ProductCategorie.objects.get(id=product_category.get('id', None))
            else:
                product.accounting_product_categorie = None

        product.save()
        return product

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.product_number = validated_data['product_number']

        # Deserialize default_unit
        default_unit = validated_data.pop('default_unit')
        if default_unit:
            if default_unit.get('id', instance.default_unit):
                instance.default_unit = Unit.objects.get(id=default_unit.get('id', None))
            else:
                instance.default_unit = instance.default_unit
        else:
            instance.default_unit = None

        # Deserialize tax
        tax = validated_data.pop('tax')
        if tax:
            if tax.get('id', instance.default_unit):
                instance.tax = Tax.objects.get(id=tax.get('id', None))
            else:
                instance.tax = instance.tax
        else:
            instance.tax = None

        # Deserialize product category
        product_category = validated_data.pop('accounting_product_categorie')
        if product_category:
            if product_category.get('id', instance.accounting_product_categorie):
                instance.accounting_product_categorie = ProductCategorie.objects.get(
                    id=product_category.get('id', None))
            else:
                instance.accounting_product_categorie = instance.accounting_product_categorie
        else:
            instance.accounting_product_categorie = None

        instance.save()
        return instance
