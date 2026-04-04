# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.crm.product.tax import Tax, OptionTax
from koalixcrm.crm.product.unit import Unit, OptionUnit
from koalixcrm.crm.product.product_type import ProductType, ProductTypeAdminView
from koalixcrm.crm.product.currency import Currency, OptionCurrency

admin.site.register(Unit, OptionUnit)
admin.site.register(Currency, OptionCurrency)
admin.site.register(Tax, OptionTax)
admin.site.register(ProductType, ProductTypeAdminView)
