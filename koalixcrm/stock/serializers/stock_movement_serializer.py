# -*- coding: utf-8 -*-
"""ADR-0011: `StockMovement` is exposed read-only via generic DRF actions
(list/retrieve). Posting a new movement goes exclusively through
`services/movement_posting.post_movement`, invoked from
`StockMovementViewSet.create()` — never through a generic `ModelSerializer`
`.save()` that would bypass the OnHandRecord/StockBalance projection."""
from __future__ import annotations

import uuid

from rest_framework import serializers

from koalixcrm.contacts.models.party import Party
from koalixcrm.core.models.unit import Unit
from koalixcrm.products.models.product_variant import ProductVariant
from koalixcrm.stock.models.batch import Batch
from koalixcrm.stock.models.handling_unit import HandlingUnit
from koalixcrm.stock.models.location import Location
from koalixcrm.stock.models.movement_reason_code import MovementReasonCode
from koalixcrm.stock.models.serial_unit import SerialUnit
from koalixcrm.stock.models.stock_movement import StockMovement


class StockMovementJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ('id',
                  'event_type',
                  'business_step',
                  'occurred_at',
                  'recorded_at',
                  'source_location',
                  'destination_location',
                  'product',
                  'variant',
                  'batch',
                  'serial_unit',
                  'handling_unit',
                  'parent_serial_unit',
                  'parent_batch',
                  'aggregation_group',
                  'qty',
                  'uom',
                  'reason_code',
                  'document_type',
                  'document_id',
                  'owner_type',
                  'owner_party',
                  'disposition',
                  'idempotency_key',
                  'compensates',
                  'created_by')
        read_only_fields = ('recorded_at',)


class StockMovementPostSerializer(serializers.Serializer):
    """Input serializer for `StockMovementViewSet.create()`: the validated
    field set accepted by `post_movement()`. Never itself writes anything —
    the view calls `post_movement(**validated_data)`."""

    event_type = serializers.ChoiceField(choices=StockMovement._meta.get_field('event_type').choices)
    business_step = serializers.ChoiceField(choices=StockMovement._meta.get_field('business_step').choices)
    occurred_at = serializers.DateTimeField()
    variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())
    source_location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), required=False, allow_null=True)
    destination_location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), required=False, allow_null=True)
    batch = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all(), required=False, allow_null=True)
    serial_unit = serializers.PrimaryKeyRelatedField(
        queryset=SerialUnit.objects.all(), required=False, allow_null=True)
    handling_unit = serializers.PrimaryKeyRelatedField(
        queryset=HandlingUnit.objects.all(), required=False, allow_null=True)
    qty = serializers.DecimalField(max_digits=18, decimal_places=4, required=False, allow_null=True)
    uom = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), required=False, allow_null=True)
    reason_code = serializers.PrimaryKeyRelatedField(
        queryset=MovementReasonCode.objects.all(), required=False, allow_null=True)
    owner_type = serializers.CharField(required=False)
    owner_party = serializers.PrimaryKeyRelatedField(
        queryset=Party.objects.all(), required=False, allow_null=True)
    disposition = serializers.CharField(required=False, allow_null=True)
    idempotency_key = serializers.UUIDField(required=False)

    def validate_idempotency_key(self, value):
        return value or uuid.uuid4()
