# -*- coding: utf-8 -*-
"""REQ-0019: `OnHandRecord` uniqueness, owner_party coupling, inactive
location rejection, serial-tracked qty=1 rule."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from koalixcrm.stock.models.choices import OwnerType
from koalixcrm.stock.models.on_hand_record import OnHandRecord
from tests.factories.contacts.contact_factory import StandardContactFactory
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_variant_factory import StandardProductVariantFactory
from tests.factories.stock.location_factory import StandardLocationFactory
from tests.factories.stock.on_hand_record_factory import StandardOnHandRecordFactory
from tests.factories.stock.serial_unit_factory import StandardSerialUnitFactory


class OnHandRecordUniquenessTest(TestCase):
    @pytest.mark.back_end_tests
    def test_two_records_same_variant_different_location_are_both_valid(self):
        variant = StandardProductVariantFactory()
        loc_a = StandardLocationFactory(code="LOC-A")
        loc_b = StandardLocationFactory(code="LOC-B")
        StandardOnHandRecordFactory(variant=variant, location=loc_a)
        StandardOnHandRecordFactory(variant=variant, location=loc_b)
        self.assertEqual(OnHandRecord.objects.filter(variant=variant).count(), 2)

    @pytest.mark.back_end_tests
    def test_exact_duplicate_combination_is_rejected(self):
        variant = StandardProductVariantFactory()
        location = StandardLocationFactory()
        StandardOnHandRecordFactory(variant=variant, location=location)
        duplicate = OnHandRecord(
            workspace=variant.workspace,
            variant=variant,
            location=location,
            owner_type=OwnerType.OWN,
            qty_on_hand=Decimal("5"),
            uom=StandardUnitFactory(),
        )
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    @pytest.mark.back_end_tests
    def test_customer_consignment_requires_owner_party(self):
        record = StandardOnHandRecordFactory.build(owner_type=OwnerType.CUSTOMER_CONSIGNMENT, owner_party=None)
        with self.assertRaises(ValidationError):
            record.full_clean()

    @pytest.mark.back_end_tests
    def test_customer_consignment_with_owner_party_is_valid(self):
        party = StandardContactFactory()
        record = StandardOnHandRecordFactory.build(
            workspace=party.workspace,
            owner_type=OwnerType.CUSTOMER_CONSIGNMENT,
            owner_party=party,
            variant=StandardProductVariantFactory(workspace=party.workspace),
            location=StandardLocationFactory(workspace=party.workspace),
            uom=StandardUnitFactory(),
        )
        record.full_clean()

    @pytest.mark.back_end_tests
    def test_inactive_location_rejects_new_on_hand_record(self):
        location = StandardLocationFactory(is_active=False)
        record = StandardOnHandRecordFactory.build(location=location, workspace=location.workspace)
        with self.assertRaises(ValidationError):
            record.full_clean()

    @pytest.mark.back_end_tests
    def test_serial_tracked_record_requires_qty_of_one(self):
        variant = StandardProductVariantFactory(tracking_mode="SERIAL")
        serial_unit = StandardSerialUnitFactory(variant=variant, workspace=variant.workspace)
        record = StandardOnHandRecordFactory.build(
            variant=variant,
            workspace=variant.workspace,
            location=StandardLocationFactory(workspace=variant.workspace),
            uom=StandardUnitFactory(),
            serial_unit=serial_unit,
            qty_on_hand=Decimal("2"),
        )
        with self.assertRaises(ValidationError):
            record.full_clean()

        record.qty_on_hand = Decimal("1")
        record.full_clean()

    @pytest.mark.back_end_tests
    def test_workspace_isolation(self):
        workspace_a = DefaultWorkspaceFactory(name="Workspace A")
        workspace_b = DefaultWorkspaceFactory(name="Workspace B")
        variant_a = StandardProductVariantFactory(workspace=workspace_a, sku="SKU-A")
        variant_b = StandardProductVariantFactory(workspace=workspace_b, sku="SKU-B")
        StandardOnHandRecordFactory(workspace=workspace_a, variant=variant_a,
                                    location=StandardLocationFactory(workspace=workspace_a))
        StandardOnHandRecordFactory(workspace=workspace_b, variant=variant_b,
                                    location=StandardLocationFactory(workspace=workspace_b))

        self.assertEqual(OnHandRecord.objects.filter(workspace=workspace_a).count(), 1)
        self.assertEqual(OnHandRecord.objects.filter(workspace=workspace_b).count(), 1)
