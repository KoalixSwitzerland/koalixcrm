# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.settings.models.currency_transform import CurrencyTransform


class CurrencyTransformJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyTransform
        fields = '__all__'
