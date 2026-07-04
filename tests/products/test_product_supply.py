# -*- coding: utf-8 -*-
"""ADR-0006, REQ-0014: `ProductSupply` — supplier-role enforcement (app
layer, not a DB constraint), multi-supplier support, uniqueness."""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from koalixcrm.products.models.product_supply import ProductSupply
from koalixcrm.products.services.product_supply_validation import (
    validate_supplier_role,
)
from tests.factories.contacts.contact_factory import StandardContactFactory
from tests.factories.contacts.supplier_factory import StandardSupplierFactory
from tests.factories.products.product_supply_factory import (
    StandardProductSupplyFactory,
)
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class ProductSupplyTest(TestCase):
    @pytest.mark.back_end_tests
    def test_supply_requires_active_supplier_role(self):
        non_supplier_party = StandardContactFactory.create()
        with self.assertRaises(ValidationError):
            validate_supplier_role(non_supplier_party)

    @pytest.mark.back_end_tests
    def test_supplier_role_party_passes_validation(self):
        supplier = StandardSupplierFactory.create()
        validate_supplier_role(supplier)  # no raise

    @pytest.mark.back_end_tests
    def test_clean_rejects_non_supplier_party(self):
        non_supplier_party = StandardContactFactory.create()
        supply = StandardProductSupplyFactory.build(supplier=non_supplier_party)
        with self.assertRaises(ValidationError):
            supply.clean()

    @pytest.mark.back_end_tests
    def test_product_can_have_multiple_supplies(self):
        product = StandardProductTypeFactory.create()
        supplier_a = StandardSupplierFactory.create()
        supplier_b = StandardSupplierFactory.create()
        StandardProductSupplyFactory.create(product=product, supplier=supplier_a)
        StandardProductSupplyFactory.create(product=product, supplier=supplier_b)
        self.assertEqual(product.supplies.count(), 2)

    @pytest.mark.back_end_tests
    def test_unique_product_supplier_combination(self):
        product = StandardProductTypeFactory.create()
        supplier = StandardSupplierFactory.create()
        StandardProductSupplyFactory.create(product=product, supplier=supplier)
        # Bypass the factory's `django_get_or_create` (which would just
        # return the existing row) to actually exercise the DB constraint.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProductSupply.objects.create(
                    workspace=product.workspace, product=product, supplier=supplier
                )
