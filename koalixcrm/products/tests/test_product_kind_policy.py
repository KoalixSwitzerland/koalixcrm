# -*- coding: utf-8 -*-
"""ADR-0019: `ProductKindPolicy` gating matrix + kind-immutability lock-set."""
import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from koalixcrm.products.models.choices import ProductKind
from koalixcrm.products.services.product_kind_policy import (
    check_gate,
    check_tracking_mode,
    is_kind_locked,
    validate_kind_change,
)
from koalixcrm.products.tests.factories.attribute_definition_factory import (
    StandardAttributeDefinitionFactory,
)
from koalixcrm.products.tests.factories.attribute_set_factory import StandardAttributeSetFactory
from koalixcrm.products.tests.factories.product_attribute_value_factories import (
    StandardProductAttributeEnumFactory,
)
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class GatingMatrixTest(TestCase):
    @pytest.mark.back_end_tests
    def test_service_profile_allowed_only_for_service(self):
        check_gate("ServiceProfile", ProductKind.SERVICE)
        with self.assertRaises(ValidationError):
            check_gate("ServiceProfile", ProductKind.TRADING_GOOD)

    @pytest.mark.back_end_tests
    def test_bom_allowed_for_manufactured_good_and_kit(self):
        check_gate("BillOfMaterials", ProductKind.MANUFACTURED_GOOD)
        check_gate("BillOfMaterials", ProductKind.KIT)
        with self.assertRaises(ValidationError):
            check_gate("BillOfMaterials", ProductKind.SERVICE)
        with self.assertRaises(ValidationError):
            check_gate("BillOfMaterials", ProductKind.RAW_MATERIAL)

    @pytest.mark.back_end_tests
    def test_production_order_allowed_for_manufactured_good_and_kit(self):
        check_gate("ProductionOrder", ProductKind.MANUFACTURED_GOOD)
        check_gate("ProductionOrder", ProductKind.KIT)
        with self.assertRaises(ValidationError):
            check_gate("ProductionOrder", ProductKind.TRADING_GOOD)

    @pytest.mark.back_end_tests
    def test_unknown_dependent_object_raises_key_error(self):
        with self.assertRaises(KeyError):
            check_gate("NotARealDependent", ProductKind.SERVICE)

    @pytest.mark.back_end_tests
    def test_tracking_mode_must_be_none_for_service(self):
        check_tracking_mode(ProductKind.SERVICE, "NONE")
        with self.assertRaises(ValidationError):
            check_tracking_mode(ProductKind.SERVICE, "BATCH")

    @pytest.mark.back_end_tests
    def test_tracking_mode_unrestricted_for_trading_good(self):
        check_tracking_mode(ProductKind.TRADING_GOOD, "BATCH")
        check_tracking_mode(ProductKind.TRADING_GOOD, "SERIAL")
        check_tracking_mode(ProductKind.TRADING_GOOD, "NONE")


class KindImmutabilityTest(TestCase):
    @pytest.mark.back_end_tests
    def test_kind_freely_changeable_when_lock_set_empty(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.TRADING_GOOD)
        self.assertFalse(is_kind_locked(product))
        validate_kind_change(product, ProductKind.TRADING_GOOD, ProductKind.MANUFACTURED_GOOD)  # no raise

    @pytest.mark.back_end_tests
    def test_no_op_kind_change_never_raises(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.TRADING_GOOD)
        validate_kind_change(product, ProductKind.TRADING_GOOD, ProductKind.TRADING_GOOD)

    @pytest.mark.back_end_tests
    def test_new_product_kind_change_never_raises(self):
        validate_kind_change(StandardProductTypeFactory.build(), None, ProductKind.MANUFACTURED_GOOD)

    @pytest.mark.back_end_tests
    def test_kind_bound_attribute_value_locks_kind(self):
        from koalixcrm.products.models.attribute_set import AttributeSetGroup
        from koalixcrm.products.tests.factories.attribute_group_factory import (
            StandardAttributeGroupFactory,
        )

        product = StandardProductTypeFactory.create(kind=ProductKind.MANUFACTURED_GOOD)
        attribute_set = StandardAttributeSetFactory.create(kind=ProductKind.MANUFACTURED_GOOD)
        group = StandardAttributeGroupFactory.create(key="kind-lock-group")
        definition = StandardAttributeDefinitionFactory.create(key="kind-lock-attr", group=group)
        AttributeSetGroup.objects.create(attribute_set=attribute_set, attribute_group=group)
        StandardProductAttributeEnumFactory.create(product=product, attribute_definition=definition, value="matt")

        self.assertTrue(is_kind_locked(product))
        with self.assertRaises(ValidationError):
            validate_kind_change(product, ProductKind.MANUFACTURED_GOOD, ProductKind.KIT)

    @pytest.mark.back_end_tests
    def test_variant_existence_does_not_lock_kind(self):
        """ADR-0019: ProductVariant is kind-agnostic and explicitly excluded
        from the lock-set."""
        from koalixcrm.products.tests.factories.product_variant_factory import (
            StandardProductVariantFactory,
        )

        product = StandardProductTypeFactory.create(kind=ProductKind.TRADING_GOOD)
        StandardProductVariantFactory.create(product=product, sku="SKU-LOCK-CHECK")
        self.assertFalse(is_kind_locked(product))

    @pytest.mark.back_end_tests
    def test_bill_of_materials_locks_kind(self):
        """ADR-0019 lock-set (Stage 3): a `BillOfMaterials` row locks `kind`."""
        from koalixcrm.products.tests.factories.bill_of_materials_factory import (
            StandardBillOfMaterialsFactory,
        )

        product = StandardProductTypeFactory.create(kind=ProductKind.MANUFACTURED_GOOD)
        StandardBillOfMaterialsFactory.create(product=product)

        self.assertTrue(is_kind_locked(product))
        with self.assertRaises(ValidationError):
            validate_kind_change(product, ProductKind.MANUFACTURED_GOOD, ProductKind.KIT)

    @pytest.mark.back_end_tests
    def test_service_profile_locks_kind(self):
        """ADR-0019 lock-set (Stage 3): a `ServiceProfile` row locks `kind`."""
        from koalixcrm.products.tests.factories.service_profile_factory import (
            StandardServiceProfileFactory,
        )

        product = StandardProductTypeFactory.create(kind=ProductKind.SERVICE)
        StandardServiceProfileFactory.create(product=product)

        self.assertTrue(is_kind_locked(product))
        with self.assertRaises(ValidationError):
            validate_kind_change(product, ProductKind.SERVICE, ProductKind.TRADING_GOOD)

    @pytest.mark.back_end_tests
    def test_product_clean_enforces_kind_immutability(self):
        from koalixcrm.products.models.attribute_set import AttributeSetGroup
        from koalixcrm.products.tests.factories.attribute_group_factory import (
            StandardAttributeGroupFactory,
        )

        product = StandardProductTypeFactory.create(kind=ProductKind.MANUFACTURED_GOOD)
        attribute_set = StandardAttributeSetFactory.create(kind=ProductKind.MANUFACTURED_GOOD)
        group = StandardAttributeGroupFactory.create(key="kind-lock-group-clean")
        definition = StandardAttributeDefinitionFactory.create(key="kind-lock-attr-clean", group=group)
        AttributeSetGroup.objects.create(attribute_set=attribute_set, attribute_group=group)
        StandardProductAttributeEnumFactory.create(product=product, attribute_definition=definition, value="matt")

        product.kind = ProductKind.KIT
        with self.assertRaises(ValidationError):
            product.full_clean()
