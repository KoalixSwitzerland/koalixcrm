# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.sales_order import SalesOrder
from koalixcrm.contracts.serializers.sales_order_serializer import SalesOrderJSONSerializer


class SalesOrderViewSet(BaseModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderJSONSerializer
