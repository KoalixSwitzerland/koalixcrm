# -*- coding: utf-8 -*-
"""
ViewSet for :class:`CommercialDocumentS3Media`.

The PDF worker POSTs a row here after uploading the rendered PDF to S3.
GET is also enabled so Django admins / other consumers can inspect media
history. PATCH/PUT/DELETE are not exposed — media rows are append-only.
"""
from __future__ import annotations

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from koalixcrm.contracts.models.commercial_document_media import (
    CommercialDocumentS3Media,
)
from koalixcrm.contracts.serializers.commercial_document_media_serializer import (
    CommercialDocumentS3MediaJSONSerializer,
)
from koalixcrm.shared.permissions import ModelPermissionsWithListView
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class CommercialDocumentMediaViewSet(
    WorkspaceScopedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CommercialDocumentS3Media.objects.all()
    serializer_class = CommercialDocumentS3MediaJSONSerializer
    permission_classes = [IsAuthenticated, ModelPermissionsWithListView]
    http_method_names = ["get", "post", "head", "options"]
