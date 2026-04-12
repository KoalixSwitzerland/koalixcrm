# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.reporting.models.resource_price import ResourcePrice
from koalixcrm.products.models.currency import Currency
from koalixcrm.products.models.unit import Unit
from koalixcrm.crm.contact.customer_group import CustomerGroup
from koalixcrm.crm.serializers.customer_group_serializer import OptionCustomerGroupJSONSerializer
from koalixcrm.products.serializers.currency_serializer import CurrencyJSONSerializer
from koalixcrm.products.serializers.unit_serializer import OptionUnitJSONSerializer


class OptionResourcePriceJSONSerializer(serializers.HyperlinkedModelSerializer):
    price = serializers.DecimalField(decimal_places=2, max_digits=5)
    unit = OptionUnitJSONSerializer()
    customer_group = OptionCustomerGroupJSONSerializer()
    currency = CurrencyJSONSerializer(allow_null=False)
    valid_from = serializers.DateField(allow_null=False)
    valid_until = serializers.DateField()

    class Meta:
        model = ResourcePrice
        fields = ('price',
                  'currency',
                  'unit',
                  'valid_from',
                  'valid_until',
                  'customer_group')


class ResourcePricesSONSerializer(serializers.HyperlinkedModelSerializer):
    price = serializers.DecimalField(decimal_places=2, max_digits=5)
    currency = CurrencyJSONSerializer(allow_null=False)
    unit = OptionUnitJSONSerializer()
    valid_from = serializers.DateField(allow_null=False)
    valid_until = serializers.DateField()
    customer_group = OptionCustomerGroupJSONSerializer()

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
