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
