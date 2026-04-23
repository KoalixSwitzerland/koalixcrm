# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.accounting.models.account import Account


class OptionAccountJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    account_number = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('id',
                  'account_number',
                  'title')


class AccountBookingSumsSerializer(serializers.ModelSerializer):
    """Per-account booking aggregates needed for FOP reports.

    The four sums are parameterised by an accounting period, supplied via the
    serializer context as ``accounting_period``. Used by the Java
    pdf-export-service to build balancesheet / profitlossstatement XML
    without re-implementing the booking arithmetic.
    """
    sum_within_accounting_period = serializers.SerializerMethodField()
    sum_through_now = serializers.SerializerMethodField()
    sum_before_accounting_period = serializers.SerializerMethodField()
    sum_total = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id',
                  'account_number',
                  'title',
                  'account_type',
                  'sum_within_accounting_period',
                  'sum_through_now',
                  'sum_before_accounting_period',
                  'sum_total')

    def _period(self):
        return self.context['accounting_period']

    def get_sum_within_accounting_period(self, obj):
        return obj.sum_of_all_bookings_within_accounting_period(self._period())

    def get_sum_through_now(self, obj):
        return obj.sum_of_all_bookings_through_now(self._period())

    def get_sum_before_accounting_period(self, obj):
        return obj.sum_of_all_bookings_before_accounting_period(self._period())

    def get_sum_total(self, obj):
        return obj.sum_of_all_bookings()


class AccountJSONSerializer(serializers.ModelSerializer):
    account_number = serializers.IntegerField(allow_null=False)
    account_type = serializers.CharField(allow_null=False)
    is_open_reliabilities_account = serializers.BooleanField()
    is_open_interest_account = serializers.BooleanField()
    is_product_inventory_activa = serializers.BooleanField()
    is_a_customer_payment_account = serializers.BooleanField()

    class Meta:
        model = Account
        fields = ('id',
                  'account_number',
                  'title',
                  'account_type',
                  'description',
                  'is_open_reliabilities_account',
                  'is_open_interest_account',
                  'is_product_inventory_activa',
                  'is_a_customer_payment_account')
        depth = 1
