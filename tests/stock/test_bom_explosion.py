# -*- coding: utf-8 -*-
"""ADR-0014: BillOfMaterialsExplosion snapshot content, nested BOM
explosion, and the soft (10) / hard (20) depth limits."""
from decimal import Decimal

import pytest
from django.test import TestCase

from koalixcrm.products.models.bill_of_materials import BillOfMaterials
from koalixcrm.products.models.bom_item import BomItem
from koalixcrm.products.models.choices import ProductKind
from koalixcrm.stock.models.bill_of_materials_explosion import BillOfMaterialsExplosion
from koalixcrm.stock.services.bom_explosion import ExplosionDepthExceeded, explode
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.products.bill_of_materials_factory import (
    StandardBillOfMaterialsFactory,
    StandardBomItemFactory,
)
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class BomExplosionTest(TestCase):
    def setUp(self):
        self.unit = StandardUnitFactory()

    @pytest.mark.back_end_tests
    def test_flat_bom_explosion_snapshot_content(self):
        bom = StandardBillOfMaterialsFactory()
        bom_item = StandardBomItemFactory(bill_of_materials=bom, quantity=Decimal("3"), unit=self.unit,
                                          scrap_pct=None)
        explode(bom)
        rows = BillOfMaterialsExplosion.objects.filter(bill_of_materials=bom)
        self.assertEqual(rows.count(), 1)
        row = rows.first()
        self.assertEqual(row.depth, 1)
        self.assertEqual(row.bom_item_id, bom_item.pk)
        self.assertEqual(row.effective_qty, Decimal("3"))
        self.assertEqual(row.bom_version, bom.version)

    @pytest.mark.back_end_tests
    def test_bom_version_bumps_on_bom_item_change(self):
        bom = StandardBillOfMaterialsFactory()
        initial_version = bom.version
        StandardBomItemFactory(bill_of_materials=bom, unit=self.unit)
        bom.refresh_from_db()
        self.assertGreater(bom.version, initial_version)

    @pytest.mark.back_end_tests
    def test_nested_bom_explosion_multiplies_quantities(self):
        parent_bom = StandardBillOfMaterialsFactory(
            product__product_type_identifier="NESTED-PARENT",
        )
        sub_assembly = StandardProductTypeFactory(
            kind=ProductKind.MANUFACTURED_GOOD, product_type_identifier="NESTED-SUB",
        )
        StandardBomItemFactory(
            bill_of_materials=parent_bom, component_product=sub_assembly,
            quantity=Decimal("2"), unit=self.unit, scrap_pct=None,
        )
        sub_bom = BillOfMaterials.objects.create(workspace=sub_assembly.workspace, product=sub_assembly)
        leaf_item = StandardBomItemFactory(
            bill_of_materials=sub_bom, quantity=Decimal("5"), unit=self.unit, scrap_pct=None,
        )

        explode(parent_bom)
        rows = BillOfMaterialsExplosion.objects.filter(bill_of_materials=parent_bom)
        self.assertEqual(rows.count(), 1)
        row = rows.first()
        self.assertEqual(row.depth, 2)
        self.assertEqual(row.bom_item_id, leaf_item.pk)
        self.assertEqual(row.effective_qty, Decimal("10"))  # 2 (parent) x 5 (sub)

    @pytest.mark.back_end_tests
    def test_hard_depth_limit_rejects(self):
        chain_length = 22
        products = [
            StandardProductTypeFactory(
                kind=ProductKind.MANUFACTURED_GOOD, product_type_identifier=f"DEPTH-{i}",
            )
            for i in range(chain_length)
        ]
        boms = [
            BillOfMaterials.objects.create(workspace=products[i].workspace, product=products[i])
            for i in range(chain_length)
        ]
        for i in range(chain_length - 1):
            BomItem.objects.create(
                workspace=products[i].workspace,
                bill_of_materials=boms[i],
                component_product=products[i + 1],
                quantity=Decimal("1"),
                unit=self.unit,
            )
        # Leaf BomItem at the end of the chain so there's something to explode.
        leaf_product = StandardProductTypeFactory(
            kind=ProductKind.RAW_MATERIAL, product_type_identifier="DEPTH-LEAF",
        )
        BomItem.objects.create(
            workspace=products[-1].workspace,
            bill_of_materials=boms[-1],
            component_product=leaf_product,
            quantity=Decimal("1"),
            unit=self.unit,
        )

        with self.assertRaises(ExplosionDepthExceeded):
            explode(boms[0])
