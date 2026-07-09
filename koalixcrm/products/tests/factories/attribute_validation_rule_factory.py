# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.attribute_validation_rule import AttributeValidationRule
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.attribute_set_factory import StandardAttributeSetFactory


class StandardAttributeValidationRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValidationRule

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    attribute_set = factory.SubFactory(StandardAttributeSetFactory)
    key = "voc-required-if-matt"
    name = "VOC content required if gloss level is matt"
    order = 0
    is_active = True
    condition = {"attribute": "gloss_level", "op": "eq", "value": "matt"}
    then = {"attribute": "voc_content", "requirement": "required"}
