# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.products.models.currency_transform import CurrencyTransform


class CurrencyTransformJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyTransform
        fields = '__all__'
