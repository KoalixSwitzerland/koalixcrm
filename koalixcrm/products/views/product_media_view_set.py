# -*- coding: utf-8 -*-
"""
ProductMediaViewSet for koalixcrm products
"""
from __future__ import annotations

from koalixcrm.products.models.product_media import ProductMedia
from koalixcrm.products.serializers.product_media_serializer import (
    ProductMediaJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductMediaViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductMediaJSONSerializer
    queryset = ProductMedia.objects.all()
