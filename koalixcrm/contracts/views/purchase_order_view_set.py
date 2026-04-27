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

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return PurchaseOrder.objects.all()
        if active is not None:
            return PurchaseOrder.objects.filter(workspace=active)
        return PurchaseOrder.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
