# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.products.models.price import Price


class PriceJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
