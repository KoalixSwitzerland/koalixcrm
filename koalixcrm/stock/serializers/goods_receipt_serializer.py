# -*- coding: utf-8 -*-
"""ADR-0017: `GoodsReceipt`/`GoodsReceiptLine` serializers. `create()`
consumes `workspace` from `validated_data` (`WorkspaceScopedViewSetMixin`
convention). Status transitions are never exposed as a plain writable
field via generic PATCH — they go through the dedicated ViewSet actions,
which call `services/goods_receipt_workflow.py`."""
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.goods_receipt import GoodsReceipt
from koalixcrm.stock.models.goods_receipt_line import GoodsReceiptLine


class GoodsReceiptLineJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsReceiptLine
        fields = ('id',
                  'goods_receipt',
                  'variant',
                  'expected_qty',
                  'received_qty',
                  'uom',
                  'batch',
                  'serial_unit',
                  'target_location',
                  'line_status',
                  'notes',
                  'posted_movement')
        read_only_fields = ('line_status', 'posted_movement')


class GoodsReceiptJSONSerializer(serializers.ModelSerializer):
    lines = GoodsReceiptLineJSONSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsReceipt
        fields = ('id',
                  'supplier_party',
                  'external_doc_ref',
                  'received_at',
                  'status',
                  'notes',
                  'created_by',
                  'created_at',
                  'lines')
        read_only_fields = ('status', 'created_at')


class GoodsReceiptIngestLineSerializer(serializers.Serializer):
    variant = serializers.IntegerField()
    expected_qty = serializers.DecimalField(max_digits=18, decimal_places=4)
    uom = serializers.IntegerField(required=False, allow_null=True)
    batch = serializers.IntegerField(required=False, allow_null=True)
    target_location = serializers.IntegerField(required=False, allow_null=True)


class GoodsReceiptIngestSerializer(serializers.Serializer):
    """`POST .../goods-receipts/ingest/` input shape (ADR-0017 §Ingestion):
    a structured JSON payload; OCR/EDI adapters produce this externally."""

    supplier_party = serializers.IntegerField()
    external_doc_ref = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    received_at = serializers.DateTimeField(required=False)
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    lines = GoodsReceiptIngestLineSerializer(many=True)
