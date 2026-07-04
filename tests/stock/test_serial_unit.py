# -*- coding: utf-8 -*-
"""REQ-0022 AC-3/AC-6: `SerialUnit` uniqueness (serial_number per variant,
global_uid per workspace) and ADR-0012 soft-delete-forever + configurable
retention floor."""
import datetime

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from koalixcrm.stock.models.serial_unit import SerialUnit
from tests.factories.products.product_variant_factory import StandardProductVariantFactory
from tests.factories.stock.retention_policy_factory import StandardRetentionPolicyFactory
from tests.factories.stock.serial_unit_factory import StandardSerialUnitFactory


class SerialUnitUniquenessTest(TestCase):
    @pytest.mark.back_end_tests
    def test_serial_number_unique_per_variant(self):
        variant = StandardProductVariantFactory()
        StandardSerialUnitFactory(variant=variant, workspace=variant.workspace, serial_number="SN-DUP")
        with self.assertRaises(ValidationError):
            StandardSerialUnitFactory.build(variant=variant, workspace=variant.workspace,
                                            serial_number="SN-DUP").full_clean()

    @pytest.mark.back_end_tests
    def test_same_serial_number_allowed_across_variants(self):
        variant_a = StandardProductVariantFactory(sku="SKU-SER-A")
        variant_b = StandardProductVariantFactory(sku="SKU-SER-B")
        StandardSerialUnitFactory(variant=variant_a, workspace=variant_a.workspace, serial_number="SHARED")
        StandardSerialUnitFactory(variant=variant_b, workspace=variant_b.workspace, serial_number="SHARED")

    @pytest.mark.back_end_tests
    def test_global_uid_unique_per_workspace(self):
        variant = StandardProductVariantFactory()
        StandardSerialUnitFactory(variant=variant, workspace=variant.workspace,
                                  serial_number="SN-1", global_uid="GUID-DUP")
        other_variant = StandardProductVariantFactory(sku="SKU-SER-C", workspace=variant.workspace)
        with self.assertRaises(ValidationError):
            StandardSerialUnitFactory.build(variant=other_variant, workspace=variant.workspace,
                                            serial_number="SN-2", global_uid="GUID-DUP").full_clean()

    @pytest.mark.back_end_tests
    def test_multiple_null_global_uid_allowed(self):
        variant = StandardProductVariantFactory()
        StandardSerialUnitFactory(variant=variant, workspace=variant.workspace,
                                  serial_number="SN-A", global_uid=None)
        StandardSerialUnitFactory(variant=variant, workspace=variant.workspace,
                                  serial_number="SN-B", global_uid=None)


class SerialUnitSoftDeleteForeverTest(TestCase):
    @pytest.mark.back_end_tests
    def test_active_unit_cannot_be_deleted(self):
        unit = StandardSerialUnitFactory()
        with self.assertRaises(ValidationError):
            unit.delete()
        self.assertTrue(SerialUnit.objects.filter(pk=unit.pk).exists())

    @pytest.mark.back_end_tests
    def test_decommissioned_unit_deletable_without_configured_floor(self):
        unit = StandardSerialUnitFactory()
        unit.decommission()
        unit.delete()
        self.assertFalse(SerialUnit.objects.filter(pk=unit.pk).exists())

    @pytest.mark.back_end_tests
    def test_decommissioned_unit_blocked_while_retention_floor_not_elapsed(self):
        unit = StandardSerialUnitFactory()
        StandardRetentionPolicyFactory(workspace=unit.workspace, serial_unit_retention_floor_days=365)
        unit.decommissioned_at = timezone.now() - datetime.timedelta(days=10)
        unit.save(update_fields=["decommissioned_at"])
        with self.assertRaises(ValidationError):
            unit.delete()
        self.assertTrue(SerialUnit.objects.filter(pk=unit.pk).exists())

    @pytest.mark.back_end_tests
    def test_decommissioned_unit_deletable_after_retention_floor_elapsed(self):
        unit = StandardSerialUnitFactory()
        StandardRetentionPolicyFactory(workspace=unit.workspace, serial_unit_retention_floor_days=30)
        unit.decommissioned_at = timezone.now() - datetime.timedelta(days=365)
        unit.save(update_fields=["decommissioned_at"])
        unit.delete()
        self.assertFalse(SerialUnit.objects.filter(pk=unit.pk).exists())
