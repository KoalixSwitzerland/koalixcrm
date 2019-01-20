# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class Product(models.Model):
    identifier = models.CharField(verbose_name=_("Product Number"),
                                  max_length=200,
                                  null=True,
                                  blank=True)
    product_type = models.ForeignKey("ProductType", on_delete=models.CASCADE, verbose_name=_("Product Type"))

