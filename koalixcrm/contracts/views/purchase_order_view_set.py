# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.contracts.serializers.purchase_order_serializer import PurchaseOrderJSONSerializer


class PurchaseOrderViewSet(BaseModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderJSONSerializer
