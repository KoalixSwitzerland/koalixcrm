# -*- coding: utf-8 -*-
"""
ProductViewSet for koalixcrm products (renamed from ProductTypeViewSet —
ADR-0003 Amendment 2026-06-27; resource path `producttype` -> `product`).
"""
from __future__ import annotations

from koalixcrm.products.models.product import Product
from koalixcrm.products.serializers.product_serializer import ProductJSONSerializer
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductJSONSerializer
    queryset = Product.objects.all()
