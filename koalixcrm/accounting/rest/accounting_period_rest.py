# -*- coding: utf-8 -*-

from rest_framework import serializers

from koalixcrm.accounting.accounting.accounting_period import AccountingPeriod
from koalixcrm.accounting.models import Account


class OptionAccountingPeriodJSONSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('id',
                  'title')


class AccountingPeriodJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountingPeriod
        fields = ('id',
                  'title',
                  'begin',
                  'end')
        depth = 1
