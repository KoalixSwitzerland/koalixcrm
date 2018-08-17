# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.accounting.accounting.account import Account


class OptionAccountJSONSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    accountNumber = serializers.IntegerField(source='account_number', read_only=True)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('id',
                  'accountNumber',
                  'title')


class AccountJSONSerializer(serializers.HyperlinkedModelSerializer):
    accountNumber = serializers.IntegerField(source='account_number', allow_null=False)
    accountType = serializers.CharField(source='account_type', allow_null=False)
    isOpenReliabilitiesAccount = serializers.BooleanField(source='is_open_reliabilities_account')
    isOpenInterestAccount = serializers.BooleanField(source='is_open_interest_account')
    isProductInventoryActiva = serializers.BooleanField(source='is_product_inventory_activa')
    isCustomerPaymentAccount = serializers.BooleanField(source='is_a_customer_payment_account')

    class Meta:
        model = Account
        fields = ('id',
                  'accountNumber',
                  'title',
                  'accountType',
                  'description',
                  'isOpenReliabilitiesAccount',
                  'isOpenInterestAccount',
                  'isProductInventoryActiva',
                  'isCustomerPaymentAccount')
        depth = 1
