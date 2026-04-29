# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.core.models.currency_transform import CurrencyTransform


class CurrencyTransformJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyTransform
        fields = '__all__'
