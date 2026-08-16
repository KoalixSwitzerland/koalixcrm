# -*- coding: utf-8 -*-
"""REQ-0022 AC-5 / ADR-0012: tracking_mode <-> Batch/SerialUnit FK coupling
enforced at the OnHandRecord application layer, for all three modes."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from koalixcrm.products.models.choices import TrackingMode
from koalixcrm.stock.services.tracking_mode_policy import enforce_tracking_mode_coupling
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory
from koalixcrm.stock.tests.factories.batch_factory import StandardBatchFactory
from koalixcrm.stock.tests.factories.location_factory import StandardLocationFactory
from koalixcrm.stock.tests.factories.on_hand_record_factory import StandardOnHandRecordFactory
from koalixcrm.stock.tests.factories.serial_unit_factory import StandardSerialUnitFactory


class TrackingModeCouplingTest(TestCase):
    @pytest.mark.back_end_tests
    def test_none_forbids_batch_and_serial(self):
        variant = StandardProductVariantFactory(tracking_mode=TrackingMode.NONE)
        enforce_tracking_mode_coupling(variant, batch=None, serial_unit=None)

        batch = StandardBatchFactory(variant=variant, workspace=variant.workspace)
        with self.assertRaises(ValidationError):
            enforce_tracking_mode_coupling(variant, batch=batch, serial_unit=None)

    @pytest.mark.back_end_tests
    def test_batch_mode_requires_batch(self):
        variant = StandardProductVariantFactory(tracking_mode=TrackingMode.BATCH)
        with self.assertRaises(ValidationError):
            enforce_tracking_mode_coupling(variant, batch=None, serial_unit=None)

        batch = StandardBatchFactory(variant=variant, workspace=variant.workspace)
        enforce_tracking_mode_coupling(variant, batch=batch, serial_unit=None)

    @pytest.mark.back_end_tests
    def test_serial_mode_requires_serial_unit(self):
        variant = StandardProductVariantFactory(tracking_mode=TrackingMode.SERIAL)
        with self.assertRaises(ValidationError):
            enforce_tracking_mode_coupling(variant, batch=None, serial_unit=None)

        serial_unit = StandardSerialUnitFactory(variant=variant, workspace=variant.workspace)
        enforce_tracking_mode_coupling(variant, batch=None, serial_unit=serial_unit)

    @pytest.mark.back_end_tests
    def test_batch_or_serial_from_another_variant_is_rejected(self):
        variant = StandardProductVariantFactory(tracking_mode=TrackingMode.BATCH)
        other_variant = StandardProductVariantFactory(sku="OTHER-SKU")
        foreign_batch = StandardBatchFactory(variant=other_variant, workspace=other_variant.workspace)
        with self.assertRaises(ValidationError):
            enforce_tracking_mode_coupling(variant, batch=foreign_batch, serial_unit=None)

    @pytest.mark.back_end_tests
    def test_on_hand_record_end_to_end_batch_mode(self):
        variant = StandardProductVariantFactory(tracking_mode=TrackingMode.BATCH)
        batch = StandardBatchFactory(variant=variant, workspace=variant.workspace)
        without_batch = StandardOnHandRecordFactory.build(
            variant=variant, workspace=variant.workspace, qty_on_hand=Decimal("3"),
        )
        with self.assertRaises(ValidationError):
            without_batch.full_clean()

        with_batch = StandardOnHandRecordFactory.build(
            variant=variant, workspace=variant.workspace, batch=batch, qty_on_hand=Decimal("3"),
            location=StandardLocationFactory(workspace=variant.workspace),
            uom=StandardUnitFactory(),
        )
        with_batch.full_clean()

    @pytest.mark.back_end_tests
    def test_service_kind_forces_tracking_mode_none(self):
        from koalixcrm.products.models.choices import ProductKind
        from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory

        service_product = StandardProductTypeFactory(kind=ProductKind.SERVICE,
                                                      product_type_identifier="SVC-TM-1")
        variant = StandardProductVariantFactory(product=service_product, sku="SVC-VARIANT-TM",
                                                workspace=service_product.workspace,
                                                tracking_mode=TrackingMode.BATCH)
        with self.assertRaises(ValidationError):
            variant.full_clean()
