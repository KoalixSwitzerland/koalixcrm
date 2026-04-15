# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.sales_document_position import SalesDocumentPosition
from koalixcrm.contracts.serializers.sales_document_position_serializer import SalesDocumentPositionJSONSerializer


class SalesDocumentPositionViewSet(BaseModelViewSet):
    queryset = SalesDocumentPosition.objects.all()
    serializer_class = SalesDocumentPositionJSONSerializer
