# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.accounting.models.product_category import ProductCategory, OptionProductCategory

admin.site.register(ProductCategory, OptionProductCategory)
