# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.serializers.invoice_serializer import InvoiceJSONSerializer
from koalixcrm.contracts.serializers.nested_commercial_document import InvoiceNestedSerializer
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin


class InvoiceViewSet(NestedDetailMixin, BaseModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceJSONSerializer
    nested_serializer_class = InvoiceNestedSerializer

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return Invoice.objects.all()
        if active is not None:
            return Invoice.objects.filter(workspace=active)
        return Invoice.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
