# -*- coding: utf-8 -*-
"""ADR-0006/REQ-0014 AC-2: validates the supplier `Party` carries an active
`supplier` `PartyRole` at the serializer layer (in addition to
`ProductSupply.clean()`), per ADR-0019's "DRF-Serializer und Service-Layer
rufen ProductKindPolicy gemeinsam auf" pattern applied to this validator."""
from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from koalixcrm.products.models.product_supply import ProductSupply
from koalixcrm.products.services.product_supply_validation import (
    validate_supplier_role,
)


class ProductSupplyJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSupply
        fields = ('id', 'product', 'supplier', 'supplier_sku', 'lead_time_days',
                  'moq', 'purchase_price', 'purchase_currency')

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        supplier = attrs.get('supplier') or (self.instance.supplier if self.instance else None)
        if supplier is not None:
            try:
                validate_supplier_role(supplier)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(exc.messages) from exc
        return attrs
