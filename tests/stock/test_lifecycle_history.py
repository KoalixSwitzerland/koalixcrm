# -*- coding: utf-8 -*-
"""ADR-0015: the five SerialUnit lifecycle query paths, built on a small
hand-constructed StockMovement history."""
import datetime
import uuid
from decimal import Decimal

import pytest
from django.test import TestCase
from django.utils import timezone

from koalixcrm.stock.models.choices import BusinessStep, Disposition, EventType, OwnerType
from koalixcrm.stock.services import lifecycle_history
from koalixcrm.stock.services.movement_posting import post_movement
from tests.factories.contacts.contact_factory import StandardContactFactory
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.stock.location_factory import StandardLocationFactory
from tests.factories.stock.serial_unit_factory import StandardSerialUnitFactory


class LifecycleHistoryTest(TestCase):
    def setUp(self):
        self.unit = StandardSerialUnitFactory()
        self.workspace = self.unit.workspace
        self.uom = StandardUnitFactory()
        self.loc_a = StandardLocationFactory(workspace=self.workspace, code="LOC-A")
        self.loc_b = StandardLocationFactory(workspace=self.workspace, code="LOC-B")
        self.party = StandardContactFactory(workspace=self.workspace)
        self.other_party = StandardContactFactory(workspace=self.workspace)
        self.t0 = timezone.now() - datetime.timedelta(days=10)

    def _post(self, **kwargs):
        base = dict(
            workspace=self.workspace, variant=self.unit.variant, serial_unit=self.unit,
            uom=self.uom, qty=None,
        )
        base.update(kwargs)
        return post_movement(**base)

    @pytest.mark.back_end_tests
    def test_full_history_orders_by_occurred_at(self):
        self._post(event_type=EventType.OBJECT_EVENT, business_step=BusinessStep.COMMISSIONING,
                   occurred_at=self.t0, destination_location=self.loc_a)
        self._post(event_type=EventType.OBJECT_EVENT, business_step=BusinessStep.INSPECTING,
                   occurred_at=self.t0 + datetime.timedelta(days=1))
        history = list(lifecycle_history.full_history(self.unit))
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].business_step, BusinessStep.COMMISSIONING)
        self.assertEqual(history[1].business_step, BusinessStep.INSPECTING)

    @pytest.mark.back_end_tests
    def test_as_built_bom_and_installed_components(self):
        component = StandardSerialUnitFactory(workspace=self.workspace, serial_number="COMP-1")
        group = uuid.uuid4()
        self._post(event_type=EventType.AGGREGATION_EVENT, business_step=BusinessStep.INSTALLING,
                   occurred_at=self.t0, serial_unit=component, parent_serial_unit=self.unit,
                   aggregation_group=group, variant=component.variant)
        as_built = list(lifecycle_history.as_built_bom(self.unit))
        self.assertEqual(len(as_built), 1)
        self.assertEqual(as_built[0].serial_unit_id, component.pk)

        installed = lifecycle_history.installed_components(self.unit)
        self.assertEqual([c.pk for c in installed], [component.pk])

        # Now remove it: no longer "currently installed".
        self._post(event_type=EventType.AGGREGATION_EVENT, business_step=BusinessStep.REMOVING,
                   occurred_at=self.t0 + datetime.timedelta(days=1), serial_unit=component,
                   parent_serial_unit=self.unit, aggregation_group=uuid.uuid4(), variant=component.variant)
        installed_after_removal = lifecycle_history.installed_components(self.unit)
        self.assertEqual(installed_after_removal, [])

    @pytest.mark.back_end_tests
    def test_who_held_it_when(self):
        self._post(event_type=EventType.OBJECT_EVENT, business_step=BusinessStep.RENTAL_OUT,
                   occurred_at=self.t0, disposition=Disposition.IN_POSSESSION,
                   owner_type=OwnerType.RENTAL, owner_party=self.party)
        self._post(event_type=EventType.OBJECT_EVENT, business_step=BusinessStep.RENTAL_RETURN,
                   occurred_at=self.t0 + datetime.timedelta(days=5), disposition=Disposition.RETURNED,
                   owner_type=OwnerType.RENTAL, owner_party=self.party)
        self._post(event_type=EventType.OBJECT_EVENT, business_step=BusinessStep.RENTAL_OUT,
                   occurred_at=self.t0 + datetime.timedelta(days=6), disposition=Disposition.IN_POSSESSION,
                   owner_type=OwnerType.RENTAL, owner_party=self.other_party)

        windows = lifecycle_history.who_held_it_when(self.unit)
        self.assertEqual(len(windows), 2)
        self.assertEqual(windows[0].holder_party_id, self.party.pk)
        self.assertIsNotNone(windows[0].holder_to)
        self.assertEqual(windows[1].holder_party_id, self.other_party.pk)
        self.assertIsNone(windows[1].holder_to)  # still held

    @pytest.mark.back_end_tests
    def test_where_was_it_when(self):
        self._post(event_type=EventType.OBJECT_EVENT, business_step=BusinessStep.RECEIVING,
                   occurred_at=self.t0, destination_location=self.loc_a)
        self._post(event_type=EventType.OBJECT_EVENT, business_step=BusinessStep.INSPECTING,
                   occurred_at=self.t0 + datetime.timedelta(days=1))  # no destination: doesn't segment
        self._post(event_type=EventType.OBJECT_EVENT, business_step=BusinessStep.SHIPPING,
                   occurred_at=self.t0 + datetime.timedelta(days=2), destination_location=self.loc_b)

        windows = lifecycle_history.where_was_it_when(self.unit)
        self.assertEqual(len(windows), 2)
        self.assertEqual(windows[0].location_id, self.loc_a.pk)
        self.assertIsNotNone(windows[0].location_to)
        self.assertEqual(windows[1].location_id, self.loc_b.pk)
        self.assertIsNone(windows[1].location_to)
