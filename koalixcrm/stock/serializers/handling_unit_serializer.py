# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.handling_unit import HandlingUnit


class HandlingUnitJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandlingUnit
        fields = ('id',
                  'sscc',
                  'parent_handling_unit',
                  'location',
                  'hu_type',
                  'is_open')
