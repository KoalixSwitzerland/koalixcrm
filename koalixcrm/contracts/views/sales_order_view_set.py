# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.contracts.models.sales_order import SalesOrder
from koalixcrm.contracts.serializers.sales_order_serializer import (
    SalesOrderJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class SalesOrderViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderJSONSerializer
