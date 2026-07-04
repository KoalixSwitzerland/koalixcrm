# -*- coding: utf-8 -*-
"""
ProductVariantViewSet for koalixcrm products
"""
from __future__ import annotations

from koalixcrm.products.models.product_variant import ProductVariant
from koalixcrm.products.serializers.product_variant_serializer import (
    ProductVariantJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductVariantViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductVariantJSONSerializer
    queryset = ProductVariant.objects.all()
