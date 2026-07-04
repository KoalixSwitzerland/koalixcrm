# -*- coding: utf-8 -*-
"""ADR-0006/REQ-0015, ADR-0019: `BillOfMaterials`/`BomItem` gating and
self-reference validation at the serializer layer, mirroring
`BillOfMaterials.clean()`/`BomItem.clean()` (ADR-0019: "DRF-Serializer und
Service-Layer rufen ProductKindPolicy gemeinsam auf")."""
from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from koalixcrm.products.models.bill_of_materials import BillOfMaterials
from koalixcrm.products.models.bom_item import BomItem
from koalixcrm.products.services.product_kind_policy import check_gate


class BillOfMaterialsJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOfMaterials
        fields = ('id', 'product', 'name', 'description')

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        product = attrs.get('product') or (self.instance.product if self.instance else None)
        if product is not None:
            try:
                check_gate("BillOfMaterials", product.kind)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(exc.messages) from exc
        return attrs


class BomItemJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = BomItem
        fields = ('id', 'bill_of_materials', 'component_product', 'quantity', 'unit',
                  'scrap_pct', 'alternative_component', 'default_component_variant')

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        bom = attrs.get('bill_of_materials') or (self.instance.bill_of_materials if self.instance else None)
        component = attrs.get('component_product') or (
            self.instance.component_product if self.instance else None
        )
        if bom is not None and component is not None and bom.product_id == component.id:
            raise serializers.ValidationError(
                "A BomItem's component product may not be the same as the parent BOM's product."
            )
        default_variant = attrs.get('default_component_variant') or (
            self.instance.default_component_variant if self.instance else None
        )
        if default_variant is not None and component is not None and default_variant.product_id != component.id:
            raise serializers.ValidationError(
                "default_component_variant must be a variant of component_product."
            )
        return attrs
