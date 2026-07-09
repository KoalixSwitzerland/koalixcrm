# -*- coding: utf-8 -*-
"""ADR-0010 Amendment OQ-0011: is_free()/free_windows() time-window ATP for
serial units, incl. the availability REST endpoint."""
import datetime

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from koalixcrm.stock.services.availability import free_windows, is_free
from koalixcrm.stock.services.reservation_lifecycle import create_reservation
from koalixcrm.stock.models.choices import ReservationKind
from koalixcrm.contacts.tests.factories.user_factory import AdminUserFactory
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory
from koalixcrm.stock.tests.factories.serial_unit_factory import StandardSerialUnitFactory


class AvailabilityTest(TestCase):
    def setUp(self):
        self.variant = StandardProductVariantFactory(tracking_mode="SERIAL")
        self.workspace = self.variant.workspace
        self.serial_unit = StandardSerialUnitFactory(variant=self.variant, workspace=self.workspace)
        self.uom = StandardUnitFactory()
        self.start = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
        self.end = datetime.datetime(2026, 1, 10, tzinfo=datetime.timezone.utc)

    @pytest.mark.back_end_tests
    def test_is_free_true_with_no_reservations(self):
        self.assertTrue(is_free(self.serial_unit, self.start, self.end))

    @pytest.mark.back_end_tests
    def test_is_free_false_when_overlapping_reservation_exists(self):
        create_reservation(
            workspace=self.workspace, variant=self.variant, kind=ReservationKind.RENTAL,
            serial_unit=self.serial_unit, uom=self.uom,
            rental_start=self.start, rental_end=self.end,
        )
        self.assertFalse(is_free(self.serial_unit, self.start, self.end))

    @pytest.mark.back_end_tests
    def test_edge_touching_windows_do_not_intersect(self):
        create_reservation(
            workspace=self.workspace, variant=self.variant, kind=ReservationKind.RENTAL,
            serial_unit=self.serial_unit, uom=self.uom,
            rental_start=self.start, rental_end=self.end,
        )
        # [end, end+5) starts exactly where the existing reservation ends -> free.
        later_start = self.end
        later_end = self.end + datetime.timedelta(days=5)
        self.assertTrue(is_free(self.serial_unit, later_start, later_end))

    @pytest.mark.back_end_tests
    def test_cancelled_reservation_does_not_block(self):
        from koalixcrm.stock.services import reservation_lifecycle

        reservation = create_reservation(
            workspace=self.workspace, variant=self.variant, kind=ReservationKind.RENTAL,
            serial_unit=self.serial_unit, uom=self.uom,
            rental_start=self.start, rental_end=self.end,
        )
        reservation_lifecycle.cancel(reservation)
        self.assertTrue(is_free(self.serial_unit, self.start, self.end))

    @pytest.mark.back_end_tests
    def test_free_windows_carves_out_the_occupied_block(self):
        create_reservation(
            workspace=self.workspace, variant=self.variant, kind=ReservationKind.RENTAL,
            serial_unit=self.serial_unit, uom=self.uom,
            rental_start=self.start + datetime.timedelta(days=2),
            rental_end=self.start + datetime.timedelta(days=4),
        )
        results = free_windows(self.variant, self.start, self.end)
        self.assertEqual(len(results), 1)
        unit, windows = results[0]
        self.assertEqual(unit.pk, self.serial_unit.pk)
        self.assertEqual(windows, [
            (self.start, self.start + datetime.timedelta(days=2)),
            (self.start + datetime.timedelta(days=4), self.end),
        ])

    @pytest.mark.back_end_tests
    def test_availability_endpoint(self):
        user = AdminUserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse(
            'variant-serial-unit-availability',
            kwargs={'workspace_id': self.workspace.pk, 'variant_id': self.variant.pk},
        )
        response = client.get(url, {"start": self.start.isoformat(), "end": self.end.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]["free"])
