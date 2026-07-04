# -*- coding: utf-8 -*-
"""ADR-0010: `StockBalance` is a read-only projection — writes happen only
via `services/movement_posting.py`/`services/reservation_lifecycle.py`."""
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.stock_balance import StockBalance


class StockBalanceJSONSerializer(serializers.ModelSerializer):
    atp = serializers.DecimalField(max_digits=18, decimal_places=4, read_only=True)

    class Meta:
        model = StockBalance
        fields = ('id',
                  'variant',
                  'location',
                  'qty_on_hand',
                  'qty_booked',
                  'qty_reserved_for_document',
                  'qty_ordered',
                  'qty_in_transit',
                  'qty_quarantine',
                  'uom',
                  'atp')
        read_only_fields = fields
