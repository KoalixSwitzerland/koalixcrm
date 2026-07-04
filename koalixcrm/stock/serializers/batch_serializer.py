# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.batch import Batch


class BatchJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ('id',
                  'variant',
                  'batch_number',
                  'supplier_lot_number',
                  'production_date',
                  'expiry_date',
                  'best_before_date',
                  'received_at',
                  'quarantine',
                  'notes')
