# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition
from koalixcrm.contracts.serializers.commercial_document_position_serializer import CommercialDocumentPositionJSONSerializer


class CommercialDocumentPositionViewSet(BaseModelViewSet):
    queryset = CommercialDocumentPosition.objects.all()
    serializer_class = CommercialDocumentPositionJSONSerializer

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return CommercialDocumentPosition.objects.all()
        if active is not None:
            return CommercialDocumentPosition.objects.filter(workspace=active)
        return CommercialDocumentPosition.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
