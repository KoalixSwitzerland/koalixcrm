# -*- coding: utf-8 -*-
"""ADR-0020: backend enforcement hook + read-only DRF exposure of
`AttributeValidationRule`."""
import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from koalixcrm.products.models.attribute_set import AttributeSetGroup
from koalixcrm.products.services.attribute_validation import enforce_attribute_rules
from tests.factories.contacts.user_factory import StaffUserFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.attribute_definition_factory import (
    StandardAttributeDefinitionFactory,
)
from tests.factories.products.attribute_group_factory import (
    StandardAttributeGroupFactory,
)
from tests.factories.products.attribute_set_factory import StandardAttributeSetFactory
from tests.factories.products.attribute_validation_rule_factory import (
    StandardAttributeValidationRuleFactory,
)
from tests.factories.products.product_attribute_value_factories import (
    StandardProductAttributeEnumFactory,
)
from tests.factories.products.product_type_factory import StandardProductTypeFactory


def _bind(attribute_set, *definitions):
    for definition in definitions:
        group = definition.group or StandardAttributeGroupFactory.create(key=f"group-for-{definition.key}")
        if definition.group_id is None:
            definition.group = group
            definition.save()
        AttributeSetGroup.objects.get_or_create(attribute_set=attribute_set, attribute_group=group)


class EnforceAttributeRulesTest(TestCase):
    @pytest.mark.back_end_tests
    def test_no_violation_passes(self):
        product = StandardProductTypeFactory.create()
        attribute_set = StandardAttributeSetFactory.create(kind=product.kind)
        gloss_def = StandardAttributeDefinitionFactory.create(key="gloss_level")
        voc_def = StandardAttributeDefinitionFactory.create(key="voc_content", data_type="int")
        _bind(attribute_set, gloss_def, voc_def)
        StandardAttributeValidationRuleFactory.create(
            attribute_set=attribute_set,
            key="voc-required-if-matt",
            condition={"attribute": "gloss_level", "op": "eq", "value": "matt"},
            then={"attribute": "voc_content", "requirement": "required"},
        )
        StandardProductAttributeEnumFactory.create(product=product, attribute_definition=gloss_def, value="matt")

        from tests.factories.products.product_attribute_value_factories import (
            StandardProductAttributeIntFactory,
        )

        StandardProductAttributeIntFactory.create(product=product, attribute_definition=voc_def, value=100)

        enforce_attribute_rules(product)  # no raise

    @pytest.mark.back_end_tests
    def test_violation_raises(self):
        product = StandardProductTypeFactory.create()
        attribute_set = StandardAttributeSetFactory.create(kind=product.kind)
        gloss_def = StandardAttributeDefinitionFactory.create(key="gloss_level_v")
        voc_def = StandardAttributeDefinitionFactory.create(key="voc_content_v", data_type="int")
        _bind(attribute_set, gloss_def, voc_def)
        StandardAttributeValidationRuleFactory.create(
            attribute_set=attribute_set,
            key="voc-required-if-matt-v",
            condition={"attribute": "gloss_level_v", "op": "eq", "value": "matt"},
            then={"attribute": "voc_content_v", "requirement": "required"},
        )
        StandardProductAttributeEnumFactory.create(product=product, attribute_definition=gloss_def, value="matt")

        with self.assertRaises(ValidationError):
            enforce_attribute_rules(product)

    @pytest.mark.back_end_tests
    def test_inactive_rule_is_not_enforced(self):
        product = StandardProductTypeFactory.create()
        attribute_set = StandardAttributeSetFactory.create(kind=product.kind)
        gloss_def = StandardAttributeDefinitionFactory.create(key="gloss_level_inactive")
        _bind(attribute_set, gloss_def)
        StandardAttributeValidationRuleFactory.create(
            attribute_set=attribute_set,
            key="inactive-rule",
            is_active=False,
            condition={"attribute": "gloss_level_inactive", "op": "eq", "value": "matt"},
            then={"attribute": "voc_content_inactive", "requirement": "required"},
        )
        StandardProductAttributeEnumFactory.create(product=product, attribute_definition=gloss_def, value="matt")

        enforce_attribute_rules(product)  # no raise: rule inactive


class AttributeValidationRuleAPITest(TestCase):
    @pytest.mark.back_end_tests
    def test_rules_exposed_read_only_via_api(self):
        workspace = DefaultWorkspaceFactory.create()
        rule = StandardAttributeValidationRuleFactory.create(workspace=workspace)
        user = StaffUserFactory.create(is_superuser=True)
        client = APIClient()
        client.force_authenticate(user=user)
        base_url = f"/koalixcrm_products/api/v1/{workspace.id}/attribute-validation-rules/"

        response = client.get(base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()
        results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload
        keys = [entry["key"] for entry in results]
        self.assertIn(rule.key, keys)

        response = client.post(
            base_url,
            data={"key": "attempted-write", "attribute_set": rule.attribute_set_id},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
