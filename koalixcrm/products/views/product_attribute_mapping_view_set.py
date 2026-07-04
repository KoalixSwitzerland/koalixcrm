# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.products.models.product_attribute_mapping import ProductAttributeMapping
from koalixcrm.products.serializers.product_attribute_mapping_serializer import (
    ProductAttributeMappingJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductAttributeMappingViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductAttributeMappingJSONSerializer
    queryset = ProductAttributeMapping.objects.all()
