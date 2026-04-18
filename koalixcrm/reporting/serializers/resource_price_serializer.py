# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.contacts.models.party_group import PartyGroup
from koalixcrm.contacts.serializers.party_serializers import PartyGroupJSONSerializer
from koalixcrm.core.models.currency import Currency
from koalixcrm.core.models.unit import Unit
from koalixcrm.core.serializers.currency_serializer import CurrencyJSONSerializer
from koalixcrm.core.serializers.unit_serializer import OptionUnitJSONSerializer
from koalixcrm.reporting.models.resource_price import ResourcePrice


class OptionResourcePriceJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    price = serializers.DecimalField(decimal_places=2, max_digits=5, required=False)
    unit = OptionUnitJSONSerializer(required=False)
    party_group = PartyGroupJSONSerializer(required=False)
    currency = CurrencyJSONSerializer(allow_null=False, required=False)
    valid_from = serializers.DateField(allow_null=False, required=False)
    valid_until = serializers.DateField(required=False)

    class Meta:
        model = ResourcePrice
        fields = ('id', 'price', 'currency', 'unit',
                  'valid_from', 'valid_until', 'party_group')


class ResourcePricesSONSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(decimal_places=2, max_digits=5)
    currency = CurrencyJSONSerializer(allow_null=False)
    unit = OptionUnitJSONSerializer()
    valid_from = serializers.DateField(allow_null=False)
    valid_until = serializers.DateField()
    party_group = PartyGroupJSONSerializer()

    class Meta:
        model = ResourcePrice
        fields = ('price', 'currency', 'unit',
                  'valid_from', 'valid_until', 'party_group')

    def create(self, validated_data):
        resource_price = ResourcePrice()
        currency = validated_data.pop('currency')
        if currency and currency.get('id'):
            resource_price.currency = Currency.objects.get(id=currency['id'])
        unit = validated_data.pop('unit')
        if unit and unit.get('id'):
            resource_price.unit = Unit.objects.get(id=unit['id'])
        resource_price.save()
        party_group = validated_data.pop('party_group', None)
        if party_group and party_group.get('id'):
            resource_price.party_group = PartyGroup.objects.get(id=party_group['id'])
        resource_price.save()
        return resource_price

    def update(self, resource_price, validated_data):
        currency = validated_data.pop('currency')
        if currency and currency.get('id'):
            resource_price.currency = Currency.objects.get(id=currency['id'])
        unit = validated_data.pop('unit')
        if unit and unit.get('id'):
            resource_price.unit = Unit.objects.get(id=unit['id'])
        resource_price.save()
        party_group = validated_data.pop('party_group', None)
        if party_group and party_group.get('id'):
            resource_price.party_group = PartyGroup.objects.get(id=party_group['id'])
        else:
            resource_price.party_group = None
        resource_price.save()
        return resource_price
