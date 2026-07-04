# -*- coding: utf-8 -*-
"""ADR-0008: `ProductPassport` — JSONB placeholder, 1:1 with `Product`,
kind-agnostic (works for every `kind`)."""
import pytest
from django.db import IntegrityError, transaction
from django.test import TestCase

from koalixcrm.products.models.choices import ProductKind
from koalixcrm.products.models.product_passport import ProductPassport
from tests.factories.products.product_passport_factory import (
    StandardProductPassportFactory,
)
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class ProductPassportTest(TestCase):
    @pytest.mark.back_end_tests
    def test_stores_arbitrary_json(self):
        passport = StandardProductPassportFactory.create(
            passport_data={"material": "steel", "recyclable": True}
        )
        passport.refresh_from_db()
        self.assertEqual(passport.passport_data["material"], "steel")
        self.assertTrue(passport.passport_data["recyclable"])

    @pytest.mark.back_end_tests
    def test_defaults_to_empty_dict(self):
        passport = StandardProductPassportFactory.create()
        self.assertEqual(passport.passport_data, {})

    @pytest.mark.back_end_tests
    def test_kind_agnostic_allowed_for_every_kind(self):
        for kind in ProductKind.values:
            product = StandardProductTypeFactory.create(
                kind=kind, product_type_identifier=f"PASSPORT-{kind}"
            )
            StandardProductPassportFactory.create(product=product)  # no raise

    @pytest.mark.back_end_tests
    def test_product_has_at_most_one_passport(self):
        product = StandardProductTypeFactory.create()
        StandardProductPassportFactory.create(product=product)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProductPassport.objects.create(workspace=product.workspace, product=product)
