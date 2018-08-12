# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Currency


class StandardCurrencyFactory(factory.Factory):
    class Meta:
        model = Currency

    description = "Swiss Francs"
    short_name = "CHF"
    rounding = 0.05
