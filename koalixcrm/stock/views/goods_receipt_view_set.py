# -*- coding: utf-8 -*-
"""ADR-0017: `GoodsReceipt` ModelViewSet plus the DRAFT/IN_PROGRESS/
COMPLETED/CANCELLED workflow actions and the structured-JSON ingestion
endpoint. All transitions route through
`services/goods_receipt_workflow.py`."""
from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.goods_receipt import GoodsReceipt
from koalixcrm.stock.serializers.goods_receipt_serializer import (
    GoodsReceiptIngestSerializer,
    GoodsReceiptJSONSerializer,
)
from koalixcrm.stock.services import goods_receipt_workflow


class GoodsReceiptViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = GoodsReceiptJSONSerializer
    queryset = GoodsReceipt.objects.all()

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        goods_receipt = self.get_object()
        try:
            goods_receipt_workflow.start(goods_receipt)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(goods_receipt).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        goods_receipt = self.get_object()
        try:
            goods_receipt_workflow.complete(goods_receipt, created_by=request.user)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(goods_receipt).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        goods_receipt = self.get_object()
        try:
            goods_receipt_workflow.cancel(goods_receipt)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(goods_receipt).data)

    @action(detail=False, methods=['post'])
    def ingest(self, request):
        """ADR-0017 §Ingestion: `POST .../goods-receipts/ingest/` accepts a
        structured JSON delivery-note payload and creates a DRAFT
        GoodsReceipt with its lines in one call."""
        from koalixcrm.contacts.models.party import Party
        from koalixcrm.core.models.unit import Unit
        from koalixcrm.products.models.product_variant import ProductVariant
        from koalixcrm.stock.models.batch import Batch
        from koalixcrm.stock.models.location import Location

        serializer = GoodsReceiptIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        active_workspace = self._resolve_workspace()
        try:
            supplier_party = Party.objects.get(pk=data['supplier_party'])
            lines = []
            for raw_line in data['lines']:
                lines.append({
                    "variant": ProductVariant.objects.get(pk=raw_line['variant']),
                    "expected_qty": raw_line['expected_qty'],
                    "uom": Unit.objects.get(pk=raw_line['uom']) if raw_line.get('uom') else None,
                    "batch": Batch.objects.get(pk=raw_line['batch']) if raw_line.get('batch') else None,
                    "target_location": (
                        Location.objects.get(pk=raw_line['target_location'])
                        if raw_line.get('target_location') else None
                    ),
                })
            goods_receipt = goods_receipt_workflow.ingest(
                workspace=active_workspace,
                supplier_party=supplier_party,
                lines=lines,
                external_doc_ref=data.get('external_doc_ref'),
                received_at=data.get('received_at'),
                notes=data.get('notes'),
                created_by=request.user,
            )
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            GoodsReceiptJSONSerializer(goods_receipt).data, status=status.HTTP_201_CREATED,
        )
