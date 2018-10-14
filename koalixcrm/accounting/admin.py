# -*- coding: utf-8 -*-

from django.contrib import admin

from koalixcrm.accounting.accounting.accounting_period import AccountingPeriod, OptionAccountingPeriod
from koalixcrm.accounting.accounting.booking import Booking, OptionBooking
from koalixcrm.accounting.accounting.account import Account, OptionAccount
from koalixcrm.accounting.accounting.product_category import ProductCategory, OptionProductCategory

admin.site.register(Account, OptionAccount)
admin.site.register(Booking, OptionBooking)
admin.site.register(ProductCategory, OptionProductCategory)
admin.site.register(AccountingPeriod, OptionAccountingPeriod)
