# -*- coding: utf-8 -*-
"""
StockBalanceViewSet for koalixcrm stock (ADR-0010). Read-only: the
aggregate is only mutated by services/movement_posting.py and
services/reservation_lifecycle.py.
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.stock_balance import StockBalance
from koalixcrm.stock.serializers.stock_balance_serializer import StockBalanceJSONSerializer


class StockBalanceViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = StockBalanceJSONSerializer
    queryset = StockBalance.objects.all()
    http_method_names = ['get', 'head', 'options']
