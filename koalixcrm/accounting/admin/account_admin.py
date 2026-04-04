# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.accounting.accounting.account import Account, OptionAccount

admin.site.register(Account, OptionAccount)
