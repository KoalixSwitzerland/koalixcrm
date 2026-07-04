# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.location import Location


class LocationJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id',
                  'parent',
                  'location_type',
                  'code',
                  'name',
                  'external_ref',
                  'is_active')
