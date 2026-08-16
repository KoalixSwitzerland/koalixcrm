# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.movement_reason_code import MovementReasonCode


class MovementReasonCodeJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementReasonCode
        fields = ('id', 'code', 'label_de', 'label_en', 'applies_to_business_steps')
