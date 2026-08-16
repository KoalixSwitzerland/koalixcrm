# -*- coding: utf-8 -*-
"""ADR-0014: read-only `BillOfMaterialsExplosion` snapshot serializer."""
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.bill_of_materials_explosion import BillOfMaterialsExplosion


class BillOfMaterialsExplosionJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOfMaterialsExplosion
        fields = ('id',
                  'bill_of_materials',
                  'bom_version',
                  'depth',
                  'bom_item',
                  'effective_qty',
                  'uom',
                  'computed_at')
        read_only_fields = fields
