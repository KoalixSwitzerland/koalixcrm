# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.unit_of_measure_conversion import (
    UnitOfMeasureConversion,
)


class UnitOfMeasureConversionJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasureConversion
        fields = ('id', 'product', 'from_unit', 'to_unit', 'factor')
