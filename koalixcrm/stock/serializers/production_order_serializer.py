# -*- coding: utf-8 -*-
"""ADR-0014: `ProductionOrder`/`ProductionOrderComponent` serializers."""
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.production_order import ProductionOrder
from koalixcrm.stock.models.production_order_component import ProductionOrderComponent


class ProductionOrderComponentJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrderComponent
        fields = ('id',
                  'production_order',
                  'bom_item',
                  'product',
                  'variant',
                  'batch',
                  'planned_qty',
                  'actual_qty',
                  'uom',
                  'reservation')
        read_only_fields = ('actual_qty', 'reservation')


class ProductionOrderJSONSerializer(serializers.ModelSerializer):
    components = ProductionOrderComponentJSONSerializer(many=True, read_only=True)

    class Meta:
        model = ProductionOrder
        fields = ('id',
                  'product',
                  'bill_of_materials',
                  'planned_qty',
                  'uom',
                  'status',
                  'planned_start',
                  'completed_at',
                  'document_type',
                  'document_id',
                  'finished_serial_unit',
                  'finished_batch',
                  'aggregation_group',
                  'last_modification',
                  'date_of_creation',
                  'components')
        read_only_fields = ('status', 'completed_at', 'finished_serial_unit', 'finished_batch',
                            'aggregation_group', 'last_modification', 'date_of_creation')
