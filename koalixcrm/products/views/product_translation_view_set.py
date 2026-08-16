# -*- coding: utf-8 -*-
"""
ProductTranslationViewSet for koalixcrm products
"""
from __future__ import annotations

from koalixcrm.products.models.product_translation import ProductTranslation
from koalixcrm.products.serializers.product_translation_serializer import (
    ProductTranslationJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductTranslationViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductTranslationJSONSerializer
    queryset = ProductTranslation.objects.all()
