# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.products.models.price import Price


class ProductPrice(Price):
    product_type = models.ForeignKey("ProductType",
                                     on_delete=models.CASCADE,
                                     verbose_name=_("Product Type"))

    def __str__(self):
        return str(self.price) + " " + str(self.currency.short_name)

    class Meta:
        app_label = "products"
        db_table = "crm_productprice"
        verbose_name = _('Product Price')
        verbose_name_plural = _('Product Prices')
