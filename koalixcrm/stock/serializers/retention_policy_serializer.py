# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.retention_policy import RetentionPolicy


class RetentionPolicyJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetentionPolicy
        fields = ('id', 'serial_unit_retention_floor_days')
