# -*- coding: utf-8 -*-
"""Factories for the six typed EAV value tables (ADR-0004)."""

import factory
from django.contrib.contenttypes.models import ContentType

from koalixcrm.products.models.product_attribute_bool import ProductAttributeBool
from koalixcrm.products.models.product_attribute_decimal import ProductAttributeDecimal
from koalixcrm.products.models.product_attribute_enum import ProductAttributeEnum
from koalixcrm.products.models.product_attribute_int import ProductAttributeInt
from koalixcrm.products.models.product_attribute_reference import (
    ProductAttributeReference,
)
from koalixcrm.products.models.product_attribute_string import ProductAttributeString
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.attribute_definition_factory import (
    StandardAttributeDefinitionFactory,
)
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class StandardProductAttributeStringFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeString

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    variant = None
    attribute_definition = factory.SubFactory(StandardAttributeDefinitionFactory)
    value = "some text"


class StandardProductAttributeIntFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeInt

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    variant = None
    attribute_definition = factory.SubFactory(StandardAttributeDefinitionFactory)
    value = 42


class StandardProductAttributeDecimalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeDecimal

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    variant = None
    attribute_definition = factory.SubFactory(StandardAttributeDefinitionFactory)
    value = "1.500000"


class StandardProductAttributeBoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeBool

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    variant = None
    attribute_definition = factory.SubFactory(StandardAttributeDefinitionFactory)
    value = True


class StandardProductAttributeEnumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeEnum

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    variant = None
    attribute_definition = factory.SubFactory(StandardAttributeDefinitionFactory)
    value = "matt"


class StandardProductAttributeReferenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeReference

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    variant = None
    attribute_definition = factory.SubFactory(StandardAttributeDefinitionFactory)
    content_type = factory.LazyFunction(
        lambda: ContentType.objects.get_for_model(StandardAttributeDefinitionFactory._meta.model)
    )
    object_id = factory.SelfAttribute("attribute_definition.id")
