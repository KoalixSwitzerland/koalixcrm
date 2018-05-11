# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.product.unit import UnitTransform
from koalixcrm.crm.contact.customergroup import CustomerGroup
from koalixcrm.crm.product.unit import ProductUnitTransform
from koalixcrm.crm.product.price import ProductPrice
import koalixcrm.crm.product.price
from koalixcrm.crm.product.attribute import AttributeSet, Attribute
from koalixcrm.crm.inlinemixin import LimitedAdminInlineMixin

class Product(models.Model):
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    product_number = models.CharField(verbose_name=_("Product Number"), max_length=30,  null=True, blank=True)
    default_unit = models.ForeignKey("Unit", verbose_name=_("Unit"))
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    last_modified_by = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"), null=True, blank="True")
    tax = models.ForeignKey("Tax", blank=False)
    accounting_product_categorie = models.ForeignKey('accounting.ProductCategorie',
                                                    verbose_name=_("Accounting Product Categorie"), null=True,
                                                    blank="True")
    attribute_set = models.ForeignKey(AttributeSet, verbose_name=_("Attribute Set"))

    def get_price(self, date, unit, customer, currency):
        prices = koalixcrm.crm.product.price.Price.objects.filter(product=self.id)
        unit_transforms = UnitTransform.objects.filter(product=self.id)
        customer_group_transforms = koalixcrm.crm.product.price.CustomerGroupTransform.objects.filter(product=self.id)
        valid_prices = list()
        for price in list(prices):
            for customerGroup in CustomerGroup.objects.filter(customer=customer):
                if price.matchesDateUnitCustomerGroupCurrency(date, unit, customerGroup, currency):
                    valid_prices.append(price.price);
                else:
                    for customerGroupTransform in customer_group_transforms:
                        if price.matchesDateUnitCustomerGroupCurrency(date, unit,
                                                                      customerGroupTransfrom.transform(customerGroup),
                                                                      currency):
                            valid_prices.append(price.price * customerGroup.factor);
                        else:
                            for unitTransfrom in list(unit_transforms):
                                if price.matchesDateUnitCustomerGroupCurrency(date,
                                                                              unitTransfrom.transfrom(unit).transform(
                                                                                      unitTransfrom),
                                                                              customerGroupTransfrom.transform(
                                                                                      customerGroup), currency):
                                    valid_prices.append(
                                        price.price * customerGroupTransform.factor * unitTransform.factor);
        if (len(valid_prices) > 0):
            lowestprice = valid_prices[0]
            for price in valid_prices:
                if (price < lowestprice):
                    lowestprice = price
            return lowestprice
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
                "customer") + ": " + self.customer.__str__() + " ," + _("currency")+ ": "+ self.currency.__str__()+ _(" and unit") + ":" + self.unit.__str__()

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)

class ProductAttributeAssociation(models.Model):
    product = models.ForeignKey(Product, related_name='related_product', blank=True, null=True)
    attribute = models.ForeignKey(Attribute, related_name='related_attribute', blank=True, null=True)
    value = models.CharField(max_length=255, verbose_name=_("Value"), blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Specific field')
        verbose_name_plural = _('Specific fields')

    def __str__(self):
        return ''

class AttributeInlineAdmin(LimitedAdminInlineMixin, admin.TabularInline):
    model = ProductAttributeAssociation
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
            'attribute', 'value',)
        }),
    )
    allow_add = True

    def get_filters(self, request, obj):
        return getattr(self, 'filters', ()) if obj is None else (('attribute', dict(attributeset=obj.id)),)

class OptionProduct(admin.ModelAdmin):
    list_display = ('product_number', 'title', 'default_unit', 'tax', 'accounting_product_categorie')
    list_display_links = ('product_number',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('product_number', 'title', 'description', 'default_unit', 'tax', 'accounting_product_categorie', 'attribute_set')
        }),)
    inlines = [ProductPrice, ProductUnitTransform, AttributeInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('attribute_set',)
        return self.readonly_fields

    def get_specific_fields(self, obj):
        fields = obj.attribute_set.attributes