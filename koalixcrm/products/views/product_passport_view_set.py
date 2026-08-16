# -*- coding: utf-8 -*-
"""ProductPassportViewSet for koalixcrm products"""
from __future__ import annotations

from koalixcrm.products.models.product_passport import ProductPassport
from koalixcrm.products.serializers.product_passport_serializer import (
    ProductPassportJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductPassportViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductPassportJSONSerializer
    queryset = ProductPassport.objects.all()
