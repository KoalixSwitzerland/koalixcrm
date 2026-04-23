# -*- coding: utf-8 -*-

from rest_framework import serializers

from koalixcrm.accounting.models.accounting_period import AccountingPeriod
from koalixcrm.accounting.models import Account
from koalixcrm.accounting.serializers.account_serializer import AccountBookingSumsSerializer


class OptionAccountingPeriodJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('id',
                  'title')


class AccountingPeriodJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingPeriod
        fields = ('id',
                  'title',
                  'begin',
                  'end')
        depth = 1


class AccountingPeriodReportSerializer(serializers.ModelSerializer):
    """Self-contained snapshot for FOP balancesheet / profitlossstatement.

    Bundles the period header, four overall aggregates, and the per-account
    sums for every account so the pdf-export-service can build the XML in a
    single fetch.
    """
    overall_earnings = serializers.SerializerMethodField()
    overall_spendings = serializers.SerializerMethodField()
    overall_assets = serializers.SerializerMethodField()
    overall_liabilities = serializers.SerializerMethodField()
    accounts = serializers.SerializerMethodField()

    class Meta:
        model = AccountingPeriod
        fields = ('id',
                  'title',
                  'begin',
                  'end',
                  'overall_earnings',
                  'overall_spendings',
                  'overall_assets',
                  'overall_liabilities',
                  'accounts')

    def get_overall_earnings(self, obj):
        return obj.overall_earnings()

    def get_overall_spendings(self, obj):
        return obj.overall_spendings()

    def get_overall_assets(self, obj):
        return obj.overall_assets()

    def get_overall_liabilities(self, obj):
        return obj.overall_liabilities()

    def get_accounts(self, obj):
        accounts = Account.objects.all()
        return AccountBookingSumsSerializer(
            accounts, many=True, context={'accounting_period': obj}
        ).data
