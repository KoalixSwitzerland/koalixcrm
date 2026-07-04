# -*- coding: utf-8 -*-
"""Serializers for the six typed EAV value tables (ADR-0004). All six
share the same shape (product, variant, attribute_definition, value[,
unit]); kept in one module to avoid boilerplate drift. Each `validate()`
re-runs the ADR-0020 declarative rule enforcement hook against the
resulting effective attribute-value set after the write would apply."""
from __future__ import annotations

from typing import Any

from rest_framework import serializers

from koalixcrm.products.models.product_attribute_bool import ProductAttributeBool
from koalixcrm.products.models.product_attribute_decimal import ProductAttributeDecimal
from koalixcrm.products.models.product_attribute_enum import ProductAttributeEnum
from koalixcrm.products.models.product_attribute_int import ProductAttributeInt
from koalixcrm.products.models.product_attribute_reference import (
    ProductAttributeReference,
)
from koalixcrm.products.models.product_attribute_string import ProductAttributeString
from koalixcrm.products.services.attribute_validation import enforce_attribute_rules


class AttributeRuleEnforcementMixin:
    """Shared `validate()` hook: re-runs the ADR-0020 rule engine against
    the product/variant's already-*persisted* effective attribute values.

    Known limitation (documented, not silently swallowed): this validates
    against the cascade as it stands *before* the current write commits,
    so a rule that only becomes satisfied/violated by the very value being
    written in this request is not caught here. Cross-attribute rules
    spanning multiple values submitted in the same request need the
    write-time value combined in; that refinement is deferred to a follow-
    up stage (see report note "ADR-0020 write-time evaluation window")."""

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        product = attrs.get('product') or getattr(self.instance, 'product', None)
        variant = attrs.get('variant', getattr(self.instance, 'variant', None))
        if product is not None:
            enforce_attribute_rules(product, variant=variant)
        return attrs


class ProductAttributeStringJSONSerializer(AttributeRuleEnforcementMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeString
        fields = (
            'id', 'product', 'variant', 'attribute_definition', 'value',
            'source_mapping', 'imported_at',
        )


class ProductAttributeIntJSONSerializer(AttributeRuleEnforcementMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeInt
        fields = (
            'id', 'product', 'variant', 'attribute_definition', 'value',
            'source_mapping', 'imported_at',
        )


class ProductAttributeDecimalJSONSerializer(AttributeRuleEnforcementMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeDecimal
        fields = (
            'id', 'product', 'variant', 'attribute_definition', 'value', 'unit',
            'source_mapping', 'imported_at',
        )


class ProductAttributeBoolJSONSerializer(AttributeRuleEnforcementMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeBool
        fields = (
            'id', 'product', 'variant', 'attribute_definition', 'value',
            'source_mapping', 'imported_at',
        )


class ProductAttributeEnumJSONSerializer(AttributeRuleEnforcementMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeEnum
        fields = (
            'id', 'product', 'variant', 'attribute_definition', 'value',
            'source_mapping', 'imported_at',
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        definition = attrs.get('attribute_definition') or getattr(self.instance, 'attribute_definition', None)
        value = attrs.get('value', getattr(self.instance, 'value', None))
        allowed = definition.enum_values if definition is not None else []
        if allowed and value not in allowed:
            raise serializers.ValidationError(
                {'value': f"{value!r} is not one of the allowed enum values {allowed!r}."}
            )
        return super().validate(attrs)


class ProductAttributeReferenceJSONSerializer(AttributeRuleEnforcementMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeReference
        fields = (
            'id', 'product', 'variant', 'attribute_definition', 'content_type', 'object_id',
            'source_mapping', 'imported_at',
        )
