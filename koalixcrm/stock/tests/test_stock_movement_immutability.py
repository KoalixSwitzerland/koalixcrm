# -*- coding: utf-8 -*-
"""ADR-0011: StockMovement rows are append-only. Also exercises the
retention-floor refusal (movement_retention.assert_deletable)."""
import datetime

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from koalixcrm.stock.models.retention_policy import RetentionPolicy
from koalixcrm.stock.services.movement_retention import assert_deletable
from koalixcrm.stock.tests.factories.stock_movement_factory import StandardStockMovementFactory


class StockMovementImmutabilityTest(TestCase):
    @pytest.mark.back_end_tests
    def test_updating_an_existing_movement_is_refused(self):
        movement = StandardStockMovementFactory()
        movement.qty = "999.0000"
        with self.assertRaises(ValidationError):
            movement.save()

    @pytest.mark.back_end_tests
    def test_deleting_a_movement_without_retention_floor_is_refused(self):
        movement = StandardStockMovementFactory()
        with self.assertRaises(ValidationError):
            assert_deletable(movement)

    @pytest.mark.back_end_tests
    def test_deleting_a_movement_before_the_retention_floor_elapses_is_refused(self):
        movement = StandardStockMovementFactory(
            occurred_at=timezone.now() - datetime.timedelta(days=1)
        )
        RetentionPolicy.objects.create(workspace=movement.workspace, stock_movement_retention_floor_days=30)
        with self.assertRaises(ValidationError):
            assert_deletable(movement)

    @pytest.mark.back_end_tests
    def test_deleting_a_movement_after_the_retention_floor_elapses_is_allowed(self):
        movement = StandardStockMovementFactory(
            occurred_at=timezone.now() - datetime.timedelta(days=100)
        )
        RetentionPolicy.objects.create(workspace=movement.workspace, stock_movement_retention_floor_days=30)
        assert_deletable(movement)  # does not raise

    @pytest.mark.back_end_tests
    def test_inventorying_movement_must_carry_null_qty(self):
        movement = StandardStockMovementFactory.build(business_step="inventorying", qty="1.0000")
        with self.assertRaises(ValidationError):
            movement.full_clean()
