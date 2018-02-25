# -*- coding: utf-8 -*-
from rest_framework import viewsets
from koalixcrm.crm.documents.salesdocumentposition import SalesDocumentPosition, SalesContractPositionJSONSerializer


class SalesContractPositionAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = SalesDocumentPosition.objects.all()
    serializer_class = SalesContractPositionJSONSerializer


