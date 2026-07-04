# -*- coding: utf-8 -*-
"""ADR-0010 Amendments OQ-0012/OQ-0013: StockReservation state machine and
first-SENT-wins concurrency rule."""
import datetime

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from koalixcrm.stock.models.choices import (
    ReservationConfirmationStatus,
    ReservationKind,
    ReservationLifecycleStatus,
)
from koalixcrm.stock.services import reservation_lifecycle
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.products.product_variant_factory import StandardProductVariantFactory
from tests.factories.stock.serial_unit_factory import StandardSerialUnitFactory


class ReservationLifecycleTest(TestCase):
    def setUp(self):
        self.variant = StandardProductVariantFactory(tracking_mode="SERIAL")
        self.workspace = self.variant.workspace
        self.serial_unit = StandardSerialUnitFactory(variant=self.variant, workspace=self.workspace)
        self.uom = StandardUnitFactory()
        self.start = timezone.now()
        self.end = self.start + datetime.timedelta(days=7)

    def _make_reservation(self, kind=ReservationKind.RENTAL, **overrides):
        params = {
            "workspace": self.workspace, "variant": self.variant, "kind": kind,
            "serial_unit": self.serial_unit, "uom": self.uom,
            "rental_start": self.start, "rental_end": self.end,
        }
        params.update(overrides)
        return reservation_lifecycle.create_reservation(**params)

    @pytest.mark.back_end_tests
    def test_create_reservation_is_active_provisional(self):
        reservation = self._make_reservation()
        self.assertEqual(reservation.status, ReservationLifecycleStatus.ACTIVE)
        self.assertEqual(reservation.reservation_status, ReservationConfirmationStatus.PROVISIONAL)

    @pytest.mark.back_end_tests
    def test_mark_sent_stamps_sent_at(self):
        reservation = self._make_reservation()
        reservation_lifecycle.mark_sent(reservation)
        reservation.refresh_from_db()
        self.assertIsNotNone(reservation.sent_at)

    @pytest.mark.back_end_tests
    def test_first_sent_wins_second_competitor_is_rejected(self):
        reservation_a = self._make_reservation()
        reservation_b = self._make_reservation()

        reservation_lifecycle.mark_sent(reservation_a)
        with self.assertRaises(reservation_lifecycle.ReservationConflict) as ctx:
            reservation_lifecycle.mark_sent(reservation_b)
        self.assertEqual(ctx.exception.colliding_reservation_id, reservation_a.pk)

    @pytest.mark.back_end_tests
    def test_non_overlapping_windows_do_not_conflict(self):
        reservation_a = self._make_reservation()
        reservation_b = self._make_reservation(
            rental_start=self.end, rental_end=self.end + datetime.timedelta(days=7)
        )
        reservation_lifecycle.mark_sent(reservation_a)
        reservation_lifecycle.mark_sent(reservation_b)  # must not raise

    @pytest.mark.back_end_tests
    def test_confirm_sets_confirmed(self):
        reservation = self._make_reservation()
        reservation_lifecycle.confirm(reservation)
        reservation.refresh_from_db()
        self.assertEqual(reservation.reservation_status, ReservationConfirmationStatus.CONFIRMED)

    @pytest.mark.back_end_tests
    def test_cancel_releases_the_reservation(self):
        reservation = self._make_reservation()
        reservation_lifecycle.cancel(reservation)
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, ReservationLifecycleStatus.CANCELLED)

    @pytest.mark.back_end_tests
    def test_fulfill_requires_active_status(self):
        reservation = self._make_reservation()
        reservation_lifecycle.cancel(reservation)
        with self.assertRaises(ValidationError):
            reservation_lifecycle.fulfill(reservation)

    @pytest.mark.back_end_tests
    def test_project_hold_and_sale_kind_semantics(self):
        project_hold = self._make_reservation(kind=ReservationKind.PROJECT_HOLD)
        self.assertEqual(project_hold.kind, ReservationKind.PROJECT_HOLD)

        sale_build = reservation_lifecycle.create_reservation(
            workspace=self.workspace, variant=self.variant, kind=ReservationKind.SALE,
            qty_reserved="3.0000", uom=self.uom,
        )
        self.assertIsNone(sale_build.serial_unit_id)
