# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.resource_price import ResourcePrice
from koalixcrm.reporting.serializers.resource_price_serializer import ResourcePricesSONSerializer


class ResourcePriceViewSet(BaseModelViewSet):
    queryset = ResourcePrice.objects.all()
    serializer_class = ResourcePricesSONSerializer
