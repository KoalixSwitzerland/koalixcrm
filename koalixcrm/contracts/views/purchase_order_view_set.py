# -*- coding: utf-8 -*-
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.contracts.serializers.nested_commercial_document import (
    PurchaseOrderNestedSerializer,
)
from koalixcrm.contracts.serializers.purchase_order_serializer import (
    PurchaseOrderJSONSerializer,
)
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class PurchaseOrderViewSet(NestedDetailMixin, BaseModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderJSONSerializer
    nested_serializer_class = PurchaseOrderNestedSerializer
