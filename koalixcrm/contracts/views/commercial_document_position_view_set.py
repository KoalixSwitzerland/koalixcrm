# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition
from koalixcrm.contracts.serializers.commercial_document_position_serializer import CommercialDocumentPositionJSONSerializer


class CommercialDocumentPositionViewSet(BaseModelViewSet):
    queryset = CommercialDocumentPosition.objects.all()
    serializer_class = CommercialDocumentPositionJSONSerializer
