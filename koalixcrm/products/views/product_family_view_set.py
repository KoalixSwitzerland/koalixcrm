# -*- coding: utf-8 -*-
"""
ProductFamilyViewSet for koalixcrm products
"""
from __future__ import annotations

from koalixcrm.products.models.product_family import ProductFamily
from koalixcrm.products.serializers.product_family_serializer import (
    ProductFamilyJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductFamilyViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductFamilyJSONSerializer
    queryset = ProductFamily.objects.all()
