# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.accounting.accounting.accounting_period import AccountingPeriod, OptionAccountingPeriod

admin.site.register(AccountingPeriod, OptionAccountingPeriod)
