# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.crm.product.price import Price


class ProductPrice(Price):
    product_type = models.ForeignKey("ProductType",
                                     on_delete=models.CASCADE,
                                     verbose_name=_("Product Type"))

    def __str__(self):
        return str(self.price) + " " + str(self.currency.short_name)

    class Meta:
        app_label = "crm"
        verbose_name = _('Product Price')
        verbose_name_plural = _('Product Prices')


class ProductPriceInlineAdminView(admin.TabularInline):
    model = ProductPrice
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
