# -*- coding: utf-8 -*-
"""ViewSets for the six typed EAV value tables (ADR-0004)."""
from __future__ import annotations

from koalixcrm.products.models.product_attribute_bool import ProductAttributeBool
from koalixcrm.products.models.product_attribute_decimal import ProductAttributeDecimal
from koalixcrm.products.models.product_attribute_enum import ProductAttributeEnum
from koalixcrm.products.models.product_attribute_int import ProductAttributeInt
from koalixcrm.products.models.product_attribute_reference import (
    ProductAttributeReference,
)
from koalixcrm.products.models.product_attribute_string import ProductAttributeString
from koalixcrm.products.serializers.product_attribute_value_serializers import (
    ProductAttributeBoolJSONSerializer,
    ProductAttributeDecimalJSONSerializer,
    ProductAttributeEnumJSONSerializer,
    ProductAttributeIntJSONSerializer,
    ProductAttributeReferenceJSONSerializer,
    ProductAttributeStringJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductAttributeStringViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductAttributeStringJSONSerializer
    queryset = ProductAttributeString.objects.all()


class ProductAttributeIntViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductAttributeIntJSONSerializer
    queryset = ProductAttributeInt.objects.all()


class ProductAttributeDecimalViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductAttributeDecimalJSONSerializer
    queryset = ProductAttributeDecimal.objects.all()


class ProductAttributeBoolViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductAttributeBoolJSONSerializer
    queryset = ProductAttributeBool.objects.all()


class ProductAttributeEnumViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductAttributeEnumJSONSerializer
    queryset = ProductAttributeEnum.objects.all()


class ProductAttributeReferenceViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductAttributeReferenceJSONSerializer
    queryset = ProductAttributeReference.objects.all()
