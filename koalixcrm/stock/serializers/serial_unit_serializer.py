# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.serial_unit import SerialUnit


class SerialUnitJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialUnit
        fields = ('id',
                  'variant',
                  'serial_number',
                  'global_uid',
                  'production_date',
                  'warranty_expiry',
                  'condition_state',
                  'batch',
                  'decommissioned_at',
                  'notes')
