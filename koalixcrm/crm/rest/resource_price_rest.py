# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.crm.reporting.resource_price import ResourcePrice
from koalixcrm.crm.product.currency import Currency
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.contact.customer_group import CustomerGroup
from koalixcrm.crm.rest.customer_group_rest import OptionCustomerGroupJSONSerializer
from koalixcrm.crm.rest.currency_rest import CurrencyJSONSerializer
from koalixcrm.crm.rest.unit_rest import OptionUnitJSONSerializer


class OptionResourcePriceJSONSerializer(serializers.HyperlinkedModelSerializer):
    price = serializers.DecimalField(source='price', decimal_places=2, max_digits=5)
    unit = OptionUnitJSONSerializer(source='unit')
    customerGroup = OptionCustomerGroupJSONSerializer(source='customer_group')
    currency = CurrencyJSONSerializer(source='currency', allow_null=False)
    validFrom = serializers.DateField(source='valid_from', allow_null=False)
    validUntil = serializers.DateField(source='valid_until')

    class Meta:
        model = ResourcePrice
        fields = ('price',
                  'currency',
                  'unit',
                  'valid_from',
                  'valid_until',
                  'customer_group')


class ResourcePricesSONSerializer(serializers.HyperlinkedModelSerializer):
    price = serializers.DecimalField(source='price', decimal_places=2, max_digits=5)
    currency = CurrencyJSONSerializer(source='currency', allow_null=False)
    unit = OptionUnitJSONSerializer(source='unit')
    validFrom = serializers.DateField(source='valid_from', allow_null=False)
    validUntil = serializers.DateField(source='valid_until')
    customerGroup = OptionCustomerGroupJSONSerializer(source='customer_group')

    class Meta:
        model = ResourcePrice
        fields = ('price',
                  'currency',
                  'unit',
                  'valid_from',
                  'valid_until',
                  'customer_group')

    def create(self, validated_data):
        resource_price = ResourcePrice()
        # Deserialize currency
        currency = validated_data.pop('currency')
        if currency:
            if currency.get('id', None):
                resource_price.currency = Currency.objects.get(id=currency.get('id', None))
            else:
                resource_price.currency = None
        # Deserialize unit
        unit = validated_data.pop('unit')
        if unit:
            if unit.get('id', None):
                resource_price.unit = Unit.objects.get(id=unit.get('id', None))
            else:
                resource_price.unit = None
        resource_price.save()
        # Deserialize customer group
        customer_group = validated_data.pop('customer_group')
        if customer_group:
            if customer_group.get('id', None):
                resource_price.customer_group = CustomerGroup.objects.get(id=customer_group.get('id', None))
            else:
                resource_price.customer_group = None
        resource_price.save()
        return resource_price

    def update(self, resource_price, validated_data):
        # Deserialize currency
        currency = validated_data.pop('currency')
        if currency:
            if currency.get('id', resource_price.currency):
                resource_price.currency = Currency.objects.get(id=currency.get('id', None))
            else:
                resource_price.currency = resource_price.currency_id
        else:
            resource_price.currency = None
        # Deserialize unit
        unit = validated_data.pop('unit')
        if unit:
            if unit.get('id', resource_price.status):
                resource_price.unit = Unit.objects.get(id=unit.get('id', None))
            else:
                resource_price.unit = resource_price.unit_id
        else:
            resource_price.unit = None
        resource_price.save()
        # Deserialize customer group
        customer_group = validated_data.pop('customer_group')
        if customer_group:
            if customer_group.get('id', resource_price.customer_group):
                resource_price.customer_group = CustomerGroup.objects.get(id=customer_group.get('id', None))
            else:
                resource_price.customer_group = resource_price.customer_group_id
        else:
            resource_price.customer_group = None
        resource_price.save()
        return resource_price



