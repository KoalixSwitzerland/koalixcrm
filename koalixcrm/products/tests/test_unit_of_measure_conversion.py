# -*- coding: utf-8 -*-
"""ADR-0005, REQ-0013: `UnitOfMeasureConversion` — product-specific unit
conversions, reversibility, uniqueness, positivity."""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from koalixcrm.products.models.unit_of_measure_conversion import (
    UnitOfMeasureConversion,
)
from koalixcrm.products.services.uom_conversion import (
    NoConversionFound,
    get_conversion_factor,
)
from koalixcrm.core.tests.factories.unit_factory import SmallUnitFactory, StandardUnitFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory
from koalixcrm.products.tests.factories.unit_of_measure_conversion_factory import (
    StandardUnitOfMeasureConversionFactory,
)


class UnitOfMeasureConversionTest(TestCase):
    @pytest.mark.back_end_tests
    def test_unique_product_from_to(self):
        product = StandardProductTypeFactory.create()
        piece = StandardUnitFactory.create()
        box = SmallUnitFactory.create()
        StandardUnitOfMeasureConversionFactory.create(product=product, from_unit=piece, to_unit=box, factor="12")
        # Bypass the factory's `django_get_or_create` (which would just
        # return the existing row) to actually exercise the DB constraint.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UnitOfMeasureConversion.objects.create(
                    workspace=product.workspace, product=product, from_unit=piece, to_unit=box, factor="24"
                )

    @pytest.mark.back_end_tests
    def test_non_positive_factor_rejected(self):
        conversion = StandardUnitOfMeasureConversionFactory.build(factor="0")
        with self.assertRaises(ValidationError):
            conversion.full_clean()

    @pytest.mark.back_end_tests
    def test_direct_conversion_factor(self):
        product = StandardProductTypeFactory.create()
        piece = StandardUnitFactory.create()
        box = SmallUnitFactory.create()
        StandardUnitOfMeasureConversionFactory.create(product=product, from_unit=piece, to_unit=box, factor="12")
        factor = get_conversion_factor(product, piece, box)
        self.assertEqual(str(factor), "12.0000000000")

    @pytest.mark.back_end_tests
    def test_reverse_conversion_is_derived(self):
        """REQ-0013 AC-2: a stored (A -> B, f) row also answers (B -> A) with 1/f."""
        product = StandardProductTypeFactory.create()
        piece = StandardUnitFactory.create()
        box = SmallUnitFactory.create()
        StandardUnitOfMeasureConversionFactory.create(product=product, from_unit=piece, to_unit=box, factor="12")
        factor = get_conversion_factor(product, box, piece)
        self.assertAlmostEqual(float(factor), 1 / 12)

    @pytest.mark.back_end_tests
    def test_same_unit_is_identity(self):
        product = StandardProductTypeFactory.create()
        piece = StandardUnitFactory.create()
        self.assertEqual(get_conversion_factor(product, piece, piece), 1)

    @pytest.mark.back_end_tests
    def test_no_conversion_found_raises(self):
        product = StandardProductTypeFactory.create()
        piece = StandardUnitFactory.create()
        box = SmallUnitFactory.create()
        with self.assertRaises(NoConversionFound):
            get_conversion_factor(product, piece, box)
