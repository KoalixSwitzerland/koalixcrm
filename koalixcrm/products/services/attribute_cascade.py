# -*- coding: utf-8 -*-
"""Read-time attribute-value cascade resolver (ADR-0004 Amendment
2026-06-28, ADR-0021): Varianten-Override -> Produkt-Wert ->
Familie-/AttributeSet-Standard. No effective value is ever materialized as
its own row; this is a pure read-time function over the typed EAV value
tables and `AttributeSetDefault`.

Justification: framework — read-time cascade resolver over EAV tables, consumed inline wherever Django needs an effective attribute value (serializers, attribute_mirror); still needed with the microservice fleet deleted.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from koalixcrm.products.models.choices import AttributeDataType

if TYPE_CHECKING:
    from koalixcrm.products.models.attribute_definition import AttributeDefinition
    from koalixcrm.products.models.product import Product
    from koalixcrm.products.models.product_variant import ProductVariant


class CascadeSource:
    OVERRIDE = "OVERRIDE"  # variant-level row
    PRODUCT = "PRODUCT"  # product-level row (variant IS NULL)
    DEFAULT = "DEFAULT"  # AttributeSetDefault (family / classification / kind)
    NONE = "NONE"  # no value anywhere in the cascade


@dataclass(frozen=True)
class ResolvedAttributeValue:
    attribute_definition_id: int
    value: Any
    source: str


_VALUE_MODEL_BY_TYPE = None


def _value_model_for(data_type: str):
    global _VALUE_MODEL_BY_TYPE
    if _VALUE_MODEL_BY_TYPE is None:
        from koalixcrm.products.models.product_attribute_bool import ProductAttributeBool
        from koalixcrm.products.models.product_attribute_decimal import (
            ProductAttributeDecimal,
        )
        from koalixcrm.products.models.product_attribute_enum import ProductAttributeEnum
        from koalixcrm.products.models.product_attribute_int import ProductAttributeInt
        from koalixcrm.products.models.product_attribute_reference import (
            ProductAttributeReference,
        )
        from koalixcrm.products.models.product_attribute_string import (
            ProductAttributeString,
        )

        _VALUE_MODEL_BY_TYPE = {
            AttributeDataType.STRING: ProductAttributeString,
            AttributeDataType.JSON: ProductAttributeString,
            AttributeDataType.INT: ProductAttributeInt,
            AttributeDataType.DECIMAL: ProductAttributeDecimal,
            AttributeDataType.MEASURE: ProductAttributeDecimal,
            AttributeDataType.BOOL: ProductAttributeBool,
            AttributeDataType.ENUM: ProductAttributeEnum,
            AttributeDataType.REFERENCE: ProductAttributeReference,
        }
    return _VALUE_MODEL_BY_TYPE[data_type]


def _coerce_default(data_type: str, raw: Any) -> Any:
    if raw is None:
        return None
    if data_type in (AttributeDataType.DECIMAL, AttributeDataType.MEASURE):
        from decimal import Decimal

        return Decimal(str(raw))
    return raw


def resolve_attribute_value(
    product: Product,
    attribute_definition: AttributeDefinition,
    variant: ProductVariant | None = None,
) -> ResolvedAttributeValue:
    """Resolve the effective value of `attribute_definition` for `product`
    (optionally scoped to `variant`) per the 3-stage cascade."""
    model = _value_model_for(attribute_definition.data_type)

    if variant is not None:
        override = model.objects.filter(
            product=product, variant=variant, attribute_definition=attribute_definition
        ).first()
        if override is not None:
            return ResolvedAttributeValue(attribute_definition.id, override.value, CascadeSource.OVERRIDE)

    product_row = model.objects.filter(
        product=product, variant__isnull=True, attribute_definition=attribute_definition
    ).first()
    if product_row is not None:
        return ResolvedAttributeValue(attribute_definition.id, product_row.value, CascadeSource.PRODUCT)

    default_value = _resolve_default(product, attribute_definition)
    if default_value is not None:
        return ResolvedAttributeValue(attribute_definition.id, default_value, CascadeSource.DEFAULT)

    return ResolvedAttributeValue(attribute_definition.id, None, CascadeSource.NONE)


def _resolve_default(product: Product, attribute_definition: AttributeDefinition) -> Any:
    """Cascade stage 3: the first matching `AttributeSetDefault` from a set
    bound to the product's family, classification nodes, or kind."""
    from koalixcrm.products.models.attribute_set import AttributeSet
    from koalixcrm.products.models.attribute_set_default import AttributeSetDefault

    candidate_sets = AttributeSet.objects.filter(workspace=product.workspace)
    node_ids = list(
        product.classifications.values_list("classification_node_id", flat=True)
    ) if hasattr(product, "classifications") else []

    from django.db.models import Q

    q = Q(kind=product.kind)
    if product.product_family_id is not None:
        q |= Q(product_family_id=product.product_family_id)
    if node_ids:
        q |= Q(classification_node_id__in=node_ids)
    candidate_sets = candidate_sets.filter(q)

    default = (
        AttributeSetDefault.objects.filter(
            attribute_set__in=candidate_sets, attribute_definition=attribute_definition
        )
        .order_by("attribute_set_id")
        .first()
    )
    if default is None:
        return None
    return _coerce_default(attribute_definition.data_type, default.default_value)
