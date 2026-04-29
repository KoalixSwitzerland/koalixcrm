# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db.models import QuerySet
from rest_framework.serializers import BaseSerializer

from koalixcrm.contracts.models.sales_order import SalesOrder
from koalixcrm.contracts.serializers.sales_order_serializer import (
    SalesOrderJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class SalesOrderViewSet(BaseModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderJSONSerializer

    def get_queryset(self) -> QuerySet[SalesOrder]:
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return SalesOrder.objects.all()
        if active is not None:
            return SalesOrder.objects.filter(workspace=active)
        return SalesOrder.objects.none()

    def perform_create(self, serializer: BaseSerializer) -> None:
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
