# -*- coding: utf-8 -*-
"""Read-only: `ProductAttributeMirror` is system-maintained via signals
(ADR-0004); the API surface exposes reads only."""
from __future__ import annotations

from rest_framework import viewsets

from koalixcrm.products.models.product_attribute_mirror import ProductAttributeMirror
from koalixcrm.products.serializers.product_attribute_mirror_serializer import (
    ProductAttributeMirrorJSONSerializer,
)
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductAttributeMirrorViewSet(WorkspaceScopedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductAttributeMirrorJSONSerializer
    queryset = ProductAttributeMirror.objects.all()
