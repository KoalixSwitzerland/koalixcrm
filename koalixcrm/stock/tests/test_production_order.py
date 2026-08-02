# -*- coding: utf-8 -*-
"""ADR-0014: ProductionOrder completion posts TRANSFORMATION_EVENT +
AGGREGATION_EVENT rows, consumes component OnHandRecord balances, and is
kind-gated to MANUFACTURED_GOOD/KIT."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from koalixcrm.products.models.choices import ProductKind
from koalixcrm.products.services.product_kind_policy import check_gate
from koalixcrm.stock.models.choices import BusinessStep, EventType, ProductionOrderStatus
from koalixcrm.stock.models.on_hand_record import OnHandRecord
from koalixcrm.stock.models.stock_movement import StockMovement
from koalixcrm.stock.services import production_order_workflow
from koalixcrm.stock.services.movement_posting import post_movement
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.products.tests.factories.bill_of_materials_factory import (
    StandardBomItemFactory,
)
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory
from koalixcrm.stock.tests.factories.location_factory import StandardLocationFactory
from koalixcrm.stock.tests.factories.production_order_factory import StandardProductionOrderFactory


class ProductionOrderWorkflowTest(TestCase):
    def setUp(self):
        self.uom = StandardUnitFactory()
        self.production_order = StandardProductionOrderFactory(planned_qty=Decimal("2"), uom=self.uom)
        self.workspace = self.production_order.workspace
        self.bom_item = StandardBomItemFactory(
            bill_of_materials=self.production_order.bill_of_materials,
            quantity=Decimal("3"), unit=self.uom, scrap_pct=None,
        )
        self.component_variant = StandardProductVariantFactory(
            product=self.bom_item.component_product, workspace=self.workspace, sku="COMP-VARIANT-1",
        )
        self.finished_variant = StandardProductVariantFactory(
            product=self.production_order.product, workspace=self.workspace, sku="FINISHED-VARIANT-1",
        )
        self.component_location = StandardLocationFactory(workspace=self.workspace, code="COMP-LOC")
        self.output_location = StandardLocationFactory(workspace=self.workspace, code="OUT-LOC")

        # Stock the component so picking can consume it.
        post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING, occurred_at=timezone.now(),
            variant=self.component_variant, destination_location=self.component_location,
            qty=Decimal("100"), uom=self.uom,
        )

    @pytest.mark.back_end_tests
    def test_kind_gating_forbids_trading_good(self):
        with self.assertRaises(ValidationError):
            check_gate("ProductionOrder", ProductKind.TRADING_GOOD)
        check_gate("ProductionOrder", ProductKind.MANUFACTURED_GOOD)
        check_gate("ProductionOrder", ProductKind.KIT)

    @pytest.mark.back_end_tests
    def test_start_resolves_component_and_reserves(self):
        production_order_workflow.release(self.production_order)
        production_order_workflow.start(self.production_order)
        self.production_order.refresh_from_db()
        self.assertEqual(self.production_order.status, ProductionOrderStatus.IN_PROGRESS)
        component = self.production_order.components.get()
        self.assertEqual(component.variant_id, self.component_variant.pk)
        self.assertEqual(component.planned_qty, Decimal("6"))  # 3 (bom) x 2 (planned_qty)
        self.assertIsNotNone(component.reservation_id)

    @pytest.mark.back_end_tests
    def test_pick_and_complete_posts_transformation_and_aggregation(self):
        production_order_workflow.release(self.production_order)
        production_order_workflow.start(self.production_order)
        production_order_workflow.pick_components(
            self.production_order, source_location=self.component_location,
        )
        component_on_hand = OnHandRecord.objects.get(
            variant=self.component_variant, location=self.component_location,
        )
        self.assertEqual(component_on_hand.qty_on_hand, Decimal("94"))  # 100 - 6

        production_order_workflow.complete(
            self.production_order,
            destination_location=self.output_location,
            finished_variant=self.finished_variant,
        )
        self.production_order.refresh_from_db()
        self.assertEqual(self.production_order.status, ProductionOrderStatus.COMPLETED)
        self.assertIsNotNone(self.production_order.aggregation_group)

        transformation = StockMovement.objects.filter(
            event_type=EventType.TRANSFORMATION_EVENT, variant=self.finished_variant,
        ).get()
        self.assertEqual(transformation.qty, Decimal("2"))
        self.assertEqual(transformation.destination_location_id, self.output_location.pk)

        aggregation_rows = StockMovement.objects.filter(
            event_type=EventType.AGGREGATION_EVENT,
            aggregation_group=self.production_order.aggregation_group,
        )
        self.assertEqual(aggregation_rows.count(), 1)
        self.assertEqual(aggregation_rows.first().variant_id, self.component_variant.pk)

        finished_on_hand = OnHandRecord.objects.get(variant=self.finished_variant, location=self.output_location)
        self.assertEqual(finished_on_hand.qty_on_hand, Decimal("2"))

    @pytest.mark.back_end_tests
    def test_complete_requires_in_progress(self):
        with self.assertRaises(ValidationError):
            production_order_workflow.complete(
                self.production_order, destination_location=self.output_location,
                finished_variant=self.finished_variant,
            )
