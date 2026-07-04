# -*- coding: utf-8 -*-
"""ADR-0010: `StockReservation` serializer; `create()` consumes `workspace`
from `validated_data` per the `WorkspaceScopedViewSetMixin` convention."""
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.choices import ReservationKind
from koalixcrm.stock.models.stock_reservation import StockReservation


class StockReservationJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockReservation
        fields = ('id',
                  'variant',
                  'location',
                  'batch',
                  'serial_unit',
                  'kind',
                  'reservation_type',
                  'reservation_status',
                  'document_type',
                  'document_id',
                  'qty_reserved',
                  'uom',
                  'rental_start',
                  'rental_end',
                  'expires_at',
                  'status',
                  'sent_at',
                  'date_of_creation',
                  'last_modification')
        read_only_fields = ('sent_at', 'date_of_creation', 'last_modification')

    def validate(self, attrs):
        kind = attrs.get('kind') or (self.instance.kind if self.instance else None)
        serial_unit = attrs.get('serial_unit') if 'serial_unit' in attrs else (
            self.instance.serial_unit if self.instance else None
        )
        if kind in (ReservationKind.RENTAL, ReservationKind.PROJECT_HOLD) and serial_unit is None:
            raise serializers.ValidationError(
                f"kind={kind} requires serial_unit to be set."
            )
        rental_start = attrs.get('rental_start') if 'rental_start' in attrs else (
            self.instance.rental_start if self.instance else None
        )
        rental_end = attrs.get('rental_end') if 'rental_end' in attrs else (
            self.instance.rental_end if self.instance else None
        )
        if rental_start is not None and rental_end is not None and rental_start >= rental_end:
            raise serializers.ValidationError("rental_start must be strictly before rental_end.")
        return attrs
