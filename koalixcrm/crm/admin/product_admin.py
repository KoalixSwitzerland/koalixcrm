# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.products.models.tax import Tax, OptionTax
from koalixcrm.products.models.unit import Unit, OptionUnit
from koalixcrm.products.models.product_type import ProductType, ProductTypeAdminView
from koalixcrm.products.models.currency import Currency, OptionCurrency

admin.site.register(Unit, OptionUnit)
admin.site.register(Currency, OptionCurrency)
admin.site.register(Tax, OptionTax)
admin.site.register(ProductType, ProductTypeAdminView)
