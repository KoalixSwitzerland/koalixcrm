# -*- coding: utf-8 -*-
"""ADR-0009/REQ-0019, ADR-0012/REQ-0022, ADR-0019: `OnHandRecord` gating,
owner-party and tracking-mode-coupling validation at the serializer layer,
mirroring `OnHandRecord.clean()` (ADR-0019: "DRF-Serializer und
Service-Layer rufen ProductKindPolicy gemeinsam auf")."""
from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from koalixcrm.products.services.product_kind_policy import check_gate
from koalixcrm.stock.models.choices import OwnerType
from koalixcrm.stock.models.on_hand_record import OnHandRecord
from koalixcrm.stock.services.tracking_mode_policy import enforce_tracking_mode_coupling


class OnHandRecordJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnHandRecord
        fields = ('id',
                  'variant',
                  'location',
                  'batch',
                  'serial_unit',
                  'handling_unit',
                  'owner_type',
                  'owner_party',
                  'qty_on_hand',
                  'uom')

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        variant = attrs.get('variant') or (self.instance.variant if self.instance else None)
        batch = attrs.get('batch') if 'batch' in attrs else (self.instance.batch if self.instance else None)
        serial_unit = attrs.get('serial_unit') if 'serial_unit' in attrs else (
            self.instance.serial_unit if self.instance else None
        )
        owner_type = attrs.get('owner_type') or (
            self.instance.owner_type if self.instance else OwnerType.OWN
        )
        owner_party = attrs.get('owner_party') if 'owner_party' in attrs else (
            self.instance.owner_party if self.instance else None
        )
        location = attrs.get('location') or (self.instance.location if self.instance else None)

        if variant is not None:
            try:
                check_gate("StockFact", variant.product.kind)
                enforce_tracking_mode_coupling(variant, batch, serial_unit)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(exc.messages) from exc

        if (owner_type in (OwnerType.CUSTOMER_CONSIGNMENT, OwnerType.RENTAL, OwnerType.CUSTOMER_OWNED)
                and owner_party is None):
            raise serializers.ValidationError(
                f"owner_type={owner_type} requires owner_party to be set."
            )
        if location is not None and not location.is_active:
            raise serializers.ValidationError(
                "Cannot create an OnHandRecord at an inactive Location."
            )
        return attrs
