# -*- coding: utf-8 -*-
"""
ViewSet for :class:`CommercialDocumentMedia`.

The PDF worker POSTs a row here after uploading the rendered PDF to S3.
GET is also enabled so Django admins / other consumers can inspect media
history. PATCH/PUT/DELETE are not exposed — media rows are append-only.
"""
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from koalixcrm.contracts.models.commercial_document_media import (
    CommercialDocumentMedia,
)
from koalixcrm.contracts.serializers.commercial_document_media_serializer import (
    CommercialDocumentMediaJSONSerializer,
)
from koalixcrm.shared.permissions import ModelPermissionsWithListView


class CommercialDocumentMediaViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CommercialDocumentMedia.objects.all()
    serializer_class = CommercialDocumentMediaJSONSerializer
    permission_classes = [IsAuthenticated, ModelPermissionsWithListView]
    http_method_names = ["get", "post", "head", "options"]
