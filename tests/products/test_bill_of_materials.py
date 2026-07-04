# -*- coding: utf-8 -*-
"""ADR-0006, REQ-0015, ADR-0019: `BillOfMaterials`/`BomItem` — ISA-95 Part 2
structure, kind gating via `ProductKindPolicy` (MANUFACTURED_GOOD and KIT
allowed), self-reference rejection, 1:1 constraint."""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from koalixcrm.products.models.bill_of_materials import BillOfMaterials
from koalixcrm.products.models.choices import ProductKind
from tests.factories.products.bill_of_materials_factory import (
    StandardBillOfMaterialsFactory,
    StandardBomItemFactory,
)
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class BillOfMaterialsGatingTest(TestCase):
    @pytest.mark.back_end_tests
    def test_bom_allowed_for_manufactured_good(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.MANUFACTURED_GOOD)
        bom = StandardBillOfMaterialsFactory.create(product=product)
        bom.full_clean()  # no raise

    @pytest.mark.back_end_tests
    def test_bom_allowed_for_kit(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.KIT)
        bom = StandardBillOfMaterialsFactory.create(product=product)
        bom.full_clean()  # no raise

    @pytest.mark.back_end_tests
    def test_bom_rejected_for_service(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.SERVICE)
        bom = StandardBillOfMaterialsFactory.build(product=product, workspace=product.workspace)
        with self.assertRaises(ValidationError):
            bom.clean()

    @pytest.mark.back_end_tests
    def test_bom_rejected_for_trading_good(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.TRADING_GOOD)
        bom = StandardBillOfMaterialsFactory.build(product=product, workspace=product.workspace)
        with self.assertRaises(ValidationError):
            bom.clean()

    @pytest.mark.back_end_tests
    def test_product_has_at_most_one_bom(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.MANUFACTURED_GOOD)
        StandardBillOfMaterialsFactory.create(product=product)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                BillOfMaterials.objects.create(workspace=product.workspace, product=product)


class BomItemTest(TestCase):
    @pytest.mark.back_end_tests
    def test_bom_item_basic_fields(self):
        item = StandardBomItemFactory.create()
        item.refresh_from_db()
        self.assertGreater(item.quantity, 0)
        self.assertIsNotNone(item.unit)

    @pytest.mark.back_end_tests
    def test_self_reference_rejected(self):
        bom = StandardBillOfMaterialsFactory.create()
        item = StandardBomItemFactory.build(
            bill_of_materials=bom, component_product=bom.product, workspace=bom.workspace
        )
        with self.assertRaises(ValidationError):
            item.clean()

    @pytest.mark.back_end_tests
    def test_alternative_component_supported(self):
        alt_product = StandardProductTypeFactory.create(kind=ProductKind.RAW_MATERIAL)
        item = StandardBomItemFactory.create(alternative_component=alt_product)
        self.assertEqual(item.alternative_component_id, alt_product.id)

    @pytest.mark.back_end_tests
    def test_default_component_variant_must_belong_to_component_product(self):
        from tests.factories.products.product_variant_factory import (
            StandardProductVariantFactory,
        )

        other_product = StandardProductTypeFactory.create(kind=ProductKind.RAW_MATERIAL)
        mismatched_variant = StandardProductVariantFactory.create(product=other_product, sku="SKU-MISMATCH")
        item = StandardBomItemFactory.create()
        item.default_component_variant = mismatched_variant
        with self.assertRaises(ValidationError):
            item.full_clean()

    @pytest.mark.back_end_tests
    def test_scrap_pct_out_of_range_rejected(self):
        item = StandardBomItemFactory.create()
        item.scrap_pct = "150.00"
        with self.assertRaises(ValidationError):
            item.full_clean()
