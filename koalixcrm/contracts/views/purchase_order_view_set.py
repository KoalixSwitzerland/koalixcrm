# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.contracts.serializers.nested_commercial_document import (
    PurchaseOrderNestedSerializer,
)
from koalixcrm.contracts.serializers.purchase_order_serializer import (
    PurchaseOrderJSONSerializer,
)
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class PurchaseOrderViewSet(WorkspaceScopedViewSetMixin, NestedDetailMixin, BaseModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderJSONSerializer
    nested_serializer_class = PurchaseOrderNestedSerializer
