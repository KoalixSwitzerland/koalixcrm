# -*- coding: utf-8 -*-
"""PriceListViewSet for koalixcrm products"""
from __future__ import annotations

from koalixcrm.products.models.price_list import PriceList
from koalixcrm.products.serializers.price_list_serializer import (
    PriceListJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class PriceListViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = PriceListJSONSerializer
    queryset = PriceList.objects.all()
