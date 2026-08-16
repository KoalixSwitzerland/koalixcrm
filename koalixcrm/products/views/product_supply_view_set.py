# -*- coding: utf-8 -*-
"""ProductSupplyViewSet for koalixcrm products"""
from __future__ import annotations

from koalixcrm.products.models.product_supply import ProductSupply
from koalixcrm.products.serializers.product_supply_serializer import (
    ProductSupplyJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductSupplyViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductSupplyJSONSerializer
    queryset = ProductSupply.objects.all()
