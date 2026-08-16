# -*- coding: utf-8 -*-
"""Keeps `ProductAttributeMirror` synchronously up to date whenever a typed
EAV value row is written or deleted (ADR-0004). Registered from
`koalixcrm.products.apps.ProductsConfig.ready()`."""
from __future__ import annotations

from django.db.models.signals import post_delete, post_save

from koalixcrm.products.models.product_attribute_bool import ProductAttributeBool
from koalixcrm.products.models.product_attribute_decimal import ProductAttributeDecimal
from koalixcrm.products.models.product_attribute_enum import ProductAttributeEnum
from koalixcrm.products.models.product_attribute_int import ProductAttributeInt
from koalixcrm.products.models.product_attribute_reference import (
    ProductAttributeReference,
)
from koalixcrm.products.models.product_attribute_string import ProductAttributeString
from koalixcrm.products.services.attribute_mirror import rebuild_attribute_mirror

_VALUE_MODELS = (
    ProductAttributeString,
    ProductAttributeInt,
    ProductAttributeDecimal,
    ProductAttributeBool,
    ProductAttributeEnum,
    ProductAttributeReference,
)


def _on_value_change(sender, instance, **kwargs) -> None:
    rebuild_attribute_mirror(instance.product, variant=None)
    if instance.variant_id is not None:
        rebuild_attribute_mirror(instance.product, variant=instance.variant)


def register_attribute_mirror_signals() -> None:
    for model in _VALUE_MODELS:
        post_save.connect(_on_value_change, sender=model, dispatch_uid=f"attr_mirror_save_{model.__name__}")
        post_delete.connect(_on_value_change, sender=model, dispatch_uid=f"attr_mirror_delete_{model.__name__}")
