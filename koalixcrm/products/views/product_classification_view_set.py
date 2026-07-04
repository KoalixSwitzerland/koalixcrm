# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.products.models.product_classification import ProductClassification
from koalixcrm.products.serializers.product_classification_serializer import (
    ProductClassificationJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductClassificationViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductClassificationJSONSerializer
    queryset = ProductClassification.objects.all()
