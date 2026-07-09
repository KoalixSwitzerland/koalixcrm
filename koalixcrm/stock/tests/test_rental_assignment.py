# -*- coding: utf-8 -*-
"""ADR-0013 (Amendment OQ-0013): RentalAssignment must reference a
fulfilled (kind=RENTAL, status=FULFILLED) StockReservation."""
import datetime

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from koalixcrm.stock.models.choices import ReservationKind, ReservationLifecycleStatus
from koalixcrm.stock.models.rental_assignment import RentalAssignment
from koalixcrm.stock.services import rental_fulfillment, reservation_lifecycle
from koalixcrm.contacts.tests.factories.contact_factory import StandardContactFactory
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory
from koalixcrm.stock.tests.factories.serial_unit_factory import StandardSerialUnitFactory
from koalixcrm.stock.tests.factories.stock_reservation_factory import RentalStockReservationFactory


class RentalAssignmentTest(TestCase):
    def setUp(self):
        self.variant = StandardProductVariantFactory(tracking_mode="SERIAL")
        self.workspace = self.variant.workspace
        self.serial_unit = StandardSerialUnitFactory(variant=self.variant, workspace=self.workspace)
        self.party = StandardContactFactory(workspace=self.workspace)
        self.uom = StandardUnitFactory()

    @pytest.mark.back_end_tests
    def test_rental_assignment_requires_fulfilled_reservation(self):
        reservation = RentalStockReservationFactory(
            workspace=self.workspace, variant=self.variant, serial_unit=self.serial_unit,
            status=ReservationLifecycleStatus.ACTIVE,
        )
        assignment = RentalAssignment(
            workspace=self.workspace,
            serial_unit=self.serial_unit,
            reservation=reservation,
            party=self.party,
            rental_start=timezone.now(),
        )
        with self.assertRaises(ValidationError):
            assignment.full_clean()

    @pytest.mark.back_end_tests
    def test_rental_assignment_requires_rental_kind_reservation(self):
        reservation = RentalStockReservationFactory(
            workspace=self.workspace, variant=self.variant, serial_unit=self.serial_unit,
            kind=ReservationKind.PROJECT_HOLD, status=ReservationLifecycleStatus.FULFILLED,
        )
        assignment = RentalAssignment(
            workspace=self.workspace,
            serial_unit=self.serial_unit,
            reservation=reservation,
            party=self.party,
            rental_start=timezone.now(),
        )
        with self.assertRaises(ValidationError):
            assignment.full_clean()

    @pytest.mark.back_end_tests
    def test_hand_over_creates_assignment_and_fulfills_reservation(self):
        reservation = reservation_lifecycle.create_reservation(
            workspace=self.workspace, variant=self.variant, kind=ReservationKind.RENTAL,
            serial_unit=self.serial_unit, uom=self.uom,
            rental_start=timezone.now(), rental_end=timezone.now() + datetime.timedelta(days=7),
        )
        assignment = rental_fulfillment.hand_over(reservation=reservation, party=self.party)
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, ReservationLifecycleStatus.FULFILLED)
        self.assertEqual(assignment.reservation_id, reservation.pk)
        self.assertEqual(assignment.serial_unit_id, self.serial_unit.pk)

    @pytest.mark.back_end_tests
    def test_return_unit_closes_out_the_assignment(self):
        reservation = reservation_lifecycle.create_reservation(
            workspace=self.workspace, variant=self.variant, kind=ReservationKind.RENTAL,
            serial_unit=self.serial_unit, uom=self.uom,
            rental_start=timezone.now(), rental_end=timezone.now() + datetime.timedelta(days=7),
        )
        assignment = rental_fulfillment.hand_over(reservation=reservation, party=self.party)
        returned = rental_fulfillment.return_unit(assignment=assignment)
        self.assertEqual(returned.status, "RETURNED")
        self.assertIsNotNone(returned.returned_at)
