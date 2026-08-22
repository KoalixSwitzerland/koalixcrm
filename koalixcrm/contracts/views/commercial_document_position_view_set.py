# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.contracts.models.commercial_document_position import (
    CommercialDocumentPosition,
)
from koalixcrm.contracts.serializers.commercial_document_position_serializer import (
    CommercialDocumentPositionJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class CommercialDocumentPositionViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = CommercialDocumentPosition.objects.all()
    serializer_class = CommercialDocumentPositionJSONSerializer
