# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.reporting.models.resource_price import ResourcePrice
from koalixcrm.reporting.serializers.resource_price_serializer import (
    ResourcePricesSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class ResourcePriceViewSet(BaseModelViewSet):
    queryset = ResourcePrice.objects.all()
    serializer_class = ResourcePricesSONSerializer
