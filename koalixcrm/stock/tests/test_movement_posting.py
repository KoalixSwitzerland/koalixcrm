# -*- coding: utf-8 -*-
"""ADR-0011: post_movement() updates OnHandRecord + StockBalance atomically
in the same transaction; inventorying is balance-neutral; a discrepant
cycle count posts a compensating adjustment; rebuild_from_log matches."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from koalixcrm.stock.models.choices import BusinessStep, EventType, OwnerType
from koalixcrm.stock.models.on_hand_record import OnHandRecord
from koalixcrm.stock.models.stock_balance import StockBalance
from koalixcrm.stock.models.stock_movement import StockMovement
from koalixcrm.stock.services.movement_posting import post_inventory_count, post_movement, rebuild_from_log
from koalixcrm.contacts.tests.factories.contact_factory import StandardContactFactory
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory
from koalixcrm.stock.tests.factories.location_factory import StandardLocationFactory


class MovementPostingTest(TestCase):
    def setUp(self):
        self.variant = StandardProductVariantFactory()
        self.workspace = self.variant.workspace
        self.location = StandardLocationFactory(workspace=self.workspace)
        self.other_location = StandardLocationFactory(workspace=self.workspace, code="LOC-OTHER")
        self.uom = StandardUnitFactory()

    @pytest.mark.back_end_tests
    def test_receiving_increases_on_hand_and_balance(self):
        post_movement(
            workspace=self.workspace,
            event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING,
            occurred_at=timezone.now(),
            variant=self.variant,
            destination_location=self.location,
            qty=Decimal("10"),
            uom=self.uom,
        )
        record = OnHandRecord.objects.get(variant=self.variant, location=self.location)
        self.assertEqual(record.qty_on_hand, Decimal("10"))
        balance = StockBalance.objects.get(variant=self.variant, location=self.location)
        self.assertEqual(balance.qty_on_hand, Decimal("10"))
        self.assertEqual(balance.atp, Decimal("10"))

    @pytest.mark.back_end_tests
    def test_shipping_decreases_on_hand_and_balance(self):
        post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING, occurred_at=timezone.now(),
            variant=self.variant, destination_location=self.location,
            qty=Decimal("10"), uom=self.uom,
        )
        post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.SHIPPING, occurred_at=timezone.now(),
            variant=self.variant, source_location=self.location,
            qty=Decimal("4"), uom=self.uom,
        )
        record = OnHandRecord.objects.get(variant=self.variant, location=self.location)
        self.assertEqual(record.qty_on_hand, Decimal("6"))
        balance = StockBalance.objects.get(variant=self.variant, location=self.location)
        self.assertEqual(balance.qty_on_hand, Decimal("6"))

    @pytest.mark.back_end_tests
    def test_overselling_rolls_back_the_whole_transaction(self):
        movement_count_before = StockMovement.objects.count()
        with self.assertRaises(ValidationError):
            post_movement(
                workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
                business_step=BusinessStep.SHIPPING, occurred_at=timezone.now(),
                variant=self.variant, source_location=self.location,
                qty=Decimal("5"), uom=self.uom,
            )
        # The StockMovement row itself must not have been committed either.
        self.assertEqual(StockMovement.objects.count(), movement_count_before)
        self.assertFalse(OnHandRecord.objects.filter(variant=self.variant, location=self.location).exists())

    @pytest.mark.back_end_tests
    def test_idempotency_key_replay_returns_the_same_movement_without_double_posting(self):
        import uuid
        key = uuid.uuid4()
        m1 = post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING, occurred_at=timezone.now(),
            variant=self.variant, destination_location=self.location,
            qty=Decimal("10"), uom=self.uom, idempotency_key=key,
        )
        m2 = post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING, occurred_at=timezone.now(),
            variant=self.variant, destination_location=self.location,
            qty=Decimal("10"), uom=self.uom, idempotency_key=key,
        )
        self.assertEqual(m1.pk, m2.pk)
        record = OnHandRecord.objects.get(variant=self.variant, location=self.location)
        self.assertEqual(record.qty_on_hand, Decimal("10"))

    @pytest.mark.back_end_tests
    def test_owner_type_segregation_customer_consignment_does_not_inflate_own_balance(self):
        party = StandardContactFactory(workspace=self.workspace)
        post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING, occurred_at=timezone.now(),
            variant=self.variant, destination_location=self.location,
            qty=Decimal("5"), uom=self.uom,
            owner_type=OwnerType.CUSTOMER_CONSIGNMENT, owner_party=party,
        )
        record = OnHandRecord.objects.get(
            variant=self.variant, location=self.location, owner_type=OwnerType.CUSTOMER_CONSIGNMENT
        )
        self.assertEqual(record.qty_on_hand, Decimal("5"))
        self.assertFalse(StockBalance.objects.filter(variant=self.variant, location=self.location).exists())

    @pytest.mark.back_end_tests
    def test_inventorying_does_not_mutate_balance(self):
        movement, adjustment = post_inventory_count(
            workspace=self.workspace, variant=self.variant, location=self.location,
            counted_qty=Decimal("0"), occurred_at=timezone.now(), uom=self.uom,
        )
        self.assertEqual(movement.business_step, BusinessStep.INVENTORYING)
        self.assertIsNone(adjustment)
        self.assertFalse(OnHandRecord.objects.filter(variant=self.variant, location=self.location).exists())
        self.assertFalse(StockBalance.objects.filter(variant=self.variant, location=self.location).exists())

    @pytest.mark.back_end_tests
    def test_inventorying_with_discrepancy_posts_a_separate_adjustment(self):
        post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING, occurred_at=timezone.now(),
            variant=self.variant, destination_location=self.location,
            qty=Decimal("10"), uom=self.uom,
        )
        movement, adjustment = post_inventory_count(
            workspace=self.workspace, variant=self.variant, location=self.location,
            counted_qty=Decimal("7"), occurred_at=timezone.now(), uom=self.uom,
        )
        self.assertEqual(movement.business_step, BusinessStep.INVENTORYING)
        self.assertIsNotNone(adjustment)
        self.assertEqual(adjustment.business_step, BusinessStep.ADJUSTMENT)
        record = OnHandRecord.objects.get(variant=self.variant, location=self.location)
        self.assertEqual(record.qty_on_hand, Decimal("7"))

    @pytest.mark.back_end_tests
    def test_rebuild_from_log_matches_after_several_movements(self):
        post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING, occurred_at=timezone.now(),
            variant=self.variant, destination_location=self.location,
            qty=Decimal("20"), uom=self.uom,
        )
        post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.SHIPPING, occurred_at=timezone.now(),
            variant=self.variant, source_location=self.location,
            qty=Decimal("3"), uom=self.uom,
        )
        report = rebuild_from_log(workspace=self.workspace)
        self.assertTrue(report["consistent"], report)

    @pytest.mark.back_end_tests
    def test_rebuild_from_log_detects_manual_drift(self):
        post_movement(
            workspace=self.workspace, event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING, occurred_at=timezone.now(),
            variant=self.variant, destination_location=self.location,
            qty=Decimal("20"), uom=self.uom,
        )
        # Simulate drift: directly mutate the aggregate outside the posting service.
        balance = StockBalance.objects.get(variant=self.variant, location=self.location)
        balance.qty_on_hand = Decimal("999")
        balance.save()

        report = rebuild_from_log(workspace=self.workspace)
        self.assertFalse(report["consistent"])
        self.assertTrue(report["balance_mismatches"])
