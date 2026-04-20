# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.despatch_advice import DespatchAdvice
from koalixcrm.contracts.serializers.despatch_advice_serializer import DespatchAdviceJSONSerializer
from koalixcrm.contracts.serializers.nested_commercial_document import DespatchAdviceNestedSerializer
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin


class DespatchAdviceViewSet(NestedDetailMixin, BaseModelViewSet):
    queryset = DespatchAdvice.objects.all()
    serializer_class = DespatchAdviceJSONSerializer
    nested_serializer_class = DespatchAdviceNestedSerializer

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return DespatchAdvice.objects.all()
        if active is not None:
            return DespatchAdvice.objects.filter(workspace=active)
        return DespatchAdvice.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
