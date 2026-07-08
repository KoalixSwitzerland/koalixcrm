# -*- coding: utf-8 -*-

import factory

from koalixcrm.accounting.models import AccountingPeriod


class StandardAccountingPeriodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccountingPeriod
        django_get_or_create = ('title',)

    title = "Fiscal Year 2018"
    begin = "2018-01-01"
    end = "2018-12-31"
    template_set_balance_sheet = None
    template_profit_loss_statement = None
