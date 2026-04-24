# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.contracts.serializers.quotation_serializer import QuotationJSONSerializer
from koalixcrm.contracts.serializers.nested_commercial_document import QuotationNestedSerializer
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin


class QuotationViewSet(NestedDetailMixin, BaseModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationJSONSerializer
    nested_serializer_class = QuotationNestedSerializer

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return Quotation.objects.all()
        if active is not None:
            return Quotation.objects.filter(workspace=active)
        return Quotation.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
