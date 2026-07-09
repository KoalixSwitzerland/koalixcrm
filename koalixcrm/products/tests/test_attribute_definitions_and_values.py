# -*- coding: utf-8 -*-
"""ADR-0004: `AttributeDefinition`/`AttributeGroup` scope invariants and
typed EAV value storage for each of the six data types."""
import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from koalixcrm.products.models.attribute_definition import AttributeDefinition
from koalixcrm.products.models.attribute_group import AttributeGroup
from koalixcrm.products.models.choices import AttributeDataType, AttributeScope
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.attribute_definition_factory import (
    StandardAttributeDefinitionFactory,
)
from koalixcrm.products.tests.factories.product_attribute_value_factories import (
    StandardProductAttributeBoolFactory,
    StandardProductAttributeDecimalFactory,
    StandardProductAttributeEnumFactory,
    StandardProductAttributeIntFactory,
    StandardProductAttributeReferenceFactory,
    StandardProductAttributeStringFactory,
)


class AttributeScopeInvariantTest(TestCase):
    @pytest.mark.back_end_tests
    def test_global_definition_rejects_workspace(self):
        workspace = DefaultWorkspaceFactory.create()
        definition = AttributeDefinition(
            workspace=workspace,
            scope=AttributeScope.GLOBAL,
            key="global-with-ws",
            label="Bad",
            data_type=AttributeDataType.STRING,
        )
        with self.assertRaises(ValidationError):
            definition.full_clean()

    @pytest.mark.back_end_tests
    def test_workspace_definition_requires_workspace(self):
        definition = AttributeDefinition(
            workspace=None,
            scope=AttributeScope.WORKSPACE,
            key="ws-without-ws",
            label="Bad",
            data_type=AttributeDataType.STRING,
        )
        with self.assertRaises(ValidationError):
            definition.full_clean()

    @pytest.mark.back_end_tests
    def test_enum_definition_requires_enum_values(self):
        definition = AttributeDefinition(
            workspace=DefaultWorkspaceFactory.create(),
            scope=AttributeScope.WORKSPACE,
            key="enum-without-values",
            label="Bad",
            data_type=AttributeDataType.ENUM,
            enum_values=[],
        )
        with self.assertRaises(ValidationError):
            definition.full_clean()

    @pytest.mark.back_end_tests
    def test_global_group_rejects_workspace(self):
        workspace = DefaultWorkspaceFactory.create()
        group = AttributeGroup(workspace=workspace, scope=AttributeScope.GLOBAL, key="bad-group", name="Bad")
        with self.assertRaises(ValidationError):
            group.full_clean()


class TypedValueStorageTest(TestCase):
    """One test per typed EAV value table (ADR-0004)."""

    @pytest.mark.back_end_tests
    def test_string_value_round_trips(self):
        row = StandardProductAttributeStringFactory.create(value="Handmade in Switzerland")
        row.refresh_from_db()
        self.assertEqual(row.value, "Handmade in Switzerland")

    @pytest.mark.back_end_tests
    def test_int_value_round_trips(self):
        row = StandardProductAttributeIntFactory.create(value=365)
        row.refresh_from_db()
        self.assertEqual(row.value, 365)

    @pytest.mark.back_end_tests
    def test_decimal_value_round_trips(self):
        row = StandardProductAttributeDecimalFactory.create(value="12.500000")
        row.refresh_from_db()
        self.assertEqual(str(row.value), "12.500000")

    @pytest.mark.back_end_tests
    def test_bool_value_round_trips(self):
        row = StandardProductAttributeBoolFactory.create(value=False)
        row.refresh_from_db()
        self.assertFalse(row.value)

    @pytest.mark.back_end_tests
    def test_enum_value_round_trips(self):
        row = StandardProductAttributeEnumFactory.create(value="satin")
        row.refresh_from_db()
        self.assertEqual(row.value, "satin")

    @pytest.mark.back_end_tests
    def test_enum_value_rejects_value_outside_allowed_set(self):
        definition = StandardAttributeDefinitionFactory.create(
            key="enum-strict", data_type=AttributeDataType.ENUM, enum_values=["a", "b"]
        )
        row = StandardProductAttributeEnumFactory.build(attribute_definition=definition, value="c")
        with self.assertRaises(ValidationError):
            row.full_clean()

    @pytest.mark.back_end_tests
    def test_reference_value_resolves_generic_fk(self):
        row = StandardProductAttributeReferenceFactory.create()
        self.assertIsNotNone(row.value)

    @pytest.mark.back_end_tests
    def test_composite_index_columns_present(self):
        """ADR-0004: every typed value table carries a composite index/
        uniqueness on (product, variant, attribute_definition)."""
        from koalixcrm.products.models.product_attribute_string import (
            ProductAttributeString,
        )

        field_names = {f.name for f in ProductAttributeString._meta.get_fields()}
        self.assertTrue({"product", "variant", "attribute_definition"}.issubset(field_names))
        constraint_names = {c.name for c in ProductAttributeString._meta.constraints}
        self.assertIn("unique_pa_string_pvad", constraint_names)
