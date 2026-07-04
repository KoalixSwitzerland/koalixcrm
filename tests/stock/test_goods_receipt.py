# -*- coding: utf-8 -*-
"""ADR-0017: GoodsReceipt status machine, completion posting, line
mismatch path, cancelled receipts post nothing, and the structured JSON
ingestion path."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from koalixcrm.stock.models.choices import GoodsReceiptLineStatus, GoodsReceiptStatus
from koalixcrm.stock.models.stock_movement import StockMovement
from koalixcrm.stock.services import goods_receipt_workflow
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.products.product_variant_factory import StandardProductVariantFactory
from tests.factories.stock.goods_receipt_factory import (
    StandardGoodsReceiptFactory,
    StandardGoodsReceiptLineFactory,
)
from tests.factories.stock.location_factory import StandardLocationFactory


class GoodsReceiptWorkflowTest(TestCase):
    def setUp(self):
        self.goods_receipt = StandardGoodsReceiptFactory()
        self.workspace = self.goods_receipt.workspace
        self.variant = StandardProductVariantFactory(workspace=self.workspace, sku="GR-VARIANT-1")
        self.uom = StandardUnitFactory()
        self.location = StandardLocationFactory(workspace=self.workspace)

    @pytest.mark.back_end_tests
    def test_status_machine_happy_path(self):
        self.assertEqual(self.goods_receipt.status, GoodsReceiptStatus.DRAFT)
        goods_receipt_workflow.start(self.goods_receipt)
        self.assertEqual(self.goods_receipt.status, GoodsReceiptStatus.IN_PROGRESS)

    @pytest.mark.back_end_tests
    def test_cannot_start_twice(self):
        goods_receipt_workflow.start(self.goods_receipt)
        with self.assertRaises(ValidationError):
            goods_receipt_workflow.start(self.goods_receipt)

    @pytest.mark.back_end_tests
    def test_complete_posts_one_movement_per_line_with_received_qty(self):
        goods_receipt_workflow.start(self.goods_receipt)
        line = StandardGoodsReceiptLineFactory(
            workspace=self.workspace, goods_receipt=self.goods_receipt, variant=self.variant,
            uom=self.uom, expected_qty=Decimal("10"), received_qty=Decimal("10"),
            target_location=self.location,
        )
        goods_receipt_workflow.complete(self.goods_receipt)

        self.goods_receipt.refresh_from_db()
        line.refresh_from_db()
        self.assertEqual(self.goods_receipt.status, GoodsReceiptStatus.COMPLETED)
        self.assertIsNotNone(line.posted_movement_id)
        movement = StockMovement.objects.get(pk=line.posted_movement_id)
        self.assertEqual(movement.business_step, "receiving")
        self.assertEqual(movement.qty, Decimal("10"))
        self.assertEqual(movement.destination_location_id, self.location.pk)

    @pytest.mark.back_end_tests
    def test_zero_received_qty_line_posts_no_movement(self):
        goods_receipt_workflow.start(self.goods_receipt)
        line = StandardGoodsReceiptLineFactory(
            workspace=self.workspace, goods_receipt=self.goods_receipt, variant=self.variant,
            uom=self.uom, expected_qty=Decimal("10"), received_qty=Decimal("0"),
            target_location=self.location,
        )
        goods_receipt_workflow.complete(self.goods_receipt)
        line.refresh_from_db()
        self.assertIsNone(line.posted_movement_id)

    @pytest.mark.back_end_tests
    def test_line_mismatch_status(self):
        line = StandardGoodsReceiptLineFactory(
            workspace=self.workspace, goods_receipt=self.goods_receipt, variant=self.variant,
            uom=self.uom, expected_qty=Decimal("10"),
        )
        goods_receipt_workflow.confirm_line(line, received_qty=Decimal("8"))
        self.assertEqual(line.line_status, GoodsReceiptLineStatus.MISMATCHED)

        line2 = StandardGoodsReceiptLineFactory(
            workspace=self.workspace, goods_receipt=self.goods_receipt, variant=self.variant,
            uom=self.uom, expected_qty=Decimal("10"),
        )
        goods_receipt_workflow.confirm_line(line2, received_qty=Decimal("10"))
        self.assertEqual(line2.line_status, GoodsReceiptLineStatus.CONFIRMED)

    @pytest.mark.back_end_tests
    def test_cancelled_receipt_posts_nothing(self):
        goods_receipt_workflow.start(self.goods_receipt)
        StandardGoodsReceiptLineFactory(
            workspace=self.workspace, goods_receipt=self.goods_receipt, variant=self.variant,
            uom=self.uom, expected_qty=Decimal("10"), received_qty=Decimal("10"),
            target_location=self.location,
        )
        before = StockMovement.objects.count()
        goods_receipt_workflow.cancel(self.goods_receipt)
        self.goods_receipt.refresh_from_db()
        self.assertEqual(self.goods_receipt.status, GoodsReceiptStatus.CANCELLED)
        self.assertEqual(StockMovement.objects.count(), before)

    @pytest.mark.back_end_tests
    def test_complete_requires_in_progress(self):
        with self.assertRaises(ValidationError):
            goods_receipt_workflow.complete(self.goods_receipt)

    @pytest.mark.back_end_tests
    def test_ingest_creates_draft_receipt_with_lines(self):
        goods_receipt = goods_receipt_workflow.ingest(
            workspace=self.workspace,
            supplier_party=self.goods_receipt.supplier_party,
            external_doc_ref="DN-INGEST-1",
            lines=[
                {"variant": self.variant, "expected_qty": Decimal("5"), "uom": self.uom},
            ],
        )
        self.assertEqual(goods_receipt.status, GoodsReceiptStatus.DRAFT)
        self.assertEqual(goods_receipt.lines.count(), 1)
        self.assertEqual(goods_receipt.lines.first().expected_qty, Decimal("5"))

    @pytest.mark.back_end_tests
    def test_missing_target_location_and_no_heuristic_raises(self):
        goods_receipt_workflow.start(self.goods_receipt)
        StandardGoodsReceiptLineFactory(
            workspace=self.workspace, goods_receipt=self.goods_receipt, variant=self.variant,
            uom=self.uom, expected_qty=Decimal("10"), received_qty=Decimal("10"),
            target_location=None,
        )
        with self.assertRaises(ValidationError):
            goods_receipt_workflow.complete(self.goods_receipt)
