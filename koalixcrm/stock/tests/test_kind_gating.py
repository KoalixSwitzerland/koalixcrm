# -*- coding: utf-8 -*-
"""ADR-0019: `ProductKindPolicy` "StockFact" gating (no stock for SERVICE)
and kind-lock-set registration for OnHandRecord/Batch/SerialUnit
(koalixcrm.stock.services.kind_lock_providers)."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from koalixcrm.products.models.choices import ProductKind
from koalixcrm.products.services.product_kind_policy import check_gate, is_kind_locked
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory
from koalixcrm.stock.tests.factories.batch_factory import StandardBatchFactory
from koalixcrm.stock.tests.factories.location_factory import StandardLocationFactory
from koalixcrm.stock.tests.factories.on_hand_record_factory import StandardOnHandRecordFactory
from koalixcrm.stock.tests.factories.serial_unit_factory import StandardSerialUnitFactory


class StockFactGatingTest(TestCase):
    @pytest.mark.back_end_tests
    def test_stock_fact_forbidden_for_service_allowed_for_others(self):
        check_gate("StockFact", ProductKind.TRADING_GOOD)
        check_gate("StockFact", ProductKind.MANUFACTURED_GOOD)
        check_gate("StockFact", ProductKind.KIT)
        check_gate("StockFact", ProductKind.RAW_MATERIAL)
        with self.assertRaises(ValidationError):
            check_gate("StockFact", ProductKind.SERVICE)

    @pytest.mark.back_end_tests
    def test_on_hand_record_rejected_for_service_product(self):
        service_product = StandardProductTypeFactory(kind=ProductKind.SERVICE,
                                                      product_type_identifier="SVC-GATE-1")
        variant = StandardProductVariantFactory(product=service_product, sku="SVC-VARIANT-GATE",
                                                workspace=service_product.workspace)
        record = StandardOnHandRecordFactory.build(
            variant=variant, workspace=variant.workspace, qty_on_hand=Decimal("1"),
            location=StandardLocationFactory(workspace=variant.workspace),
        )
        with self.assertRaises(ValidationError):
            record.full_clean()

    @pytest.mark.back_end_tests
    def test_on_hand_record_existence_locks_product_kind(self):
        product = StandardProductTypeFactory(kind=ProductKind.TRADING_GOOD,
                                              product_type_identifier="LOCK-OHR-1")
        variant = StandardProductVariantFactory(product=product, sku="LOCK-OHR-VARIANT",
                                                workspace=product.workspace)
        self.assertFalse(is_kind_locked(product))
        StandardOnHandRecordFactory(variant=variant, workspace=product.workspace)
        self.assertTrue(is_kind_locked(product))

    @pytest.mark.back_end_tests
    def test_batch_existence_locks_product_kind(self):
        product = StandardProductTypeFactory(kind=ProductKind.TRADING_GOOD,
                                              product_type_identifier="LOCK-BATCH-1")
        variant = StandardProductVariantFactory(product=product, sku="LOCK-BATCH-VARIANT",
                                                workspace=product.workspace)
        self.assertFalse(is_kind_locked(product))
        StandardBatchFactory(variant=variant, workspace=product.workspace)
        self.assertTrue(is_kind_locked(product))

    @pytest.mark.back_end_tests
    def test_serial_unit_existence_locks_product_kind(self):
        product = StandardProductTypeFactory(kind=ProductKind.TRADING_GOOD,
                                              product_type_identifier="LOCK-SERIAL-1")
        variant = StandardProductVariantFactory(product=product, sku="LOCK-SERIAL-VARIANT",
                                                workspace=product.workspace)
        self.assertFalse(is_kind_locked(product))
        StandardSerialUnitFactory(variant=variant, workspace=product.workspace)
        self.assertTrue(is_kind_locked(product))
