# -*- coding: utf-8 -*-
"""
ViewSet exposing :class:`PDFExportProcess` to the PDF microservice.

Only the lifecycle columns (``status`` / ``result_url`` / ``error_message``)
are writable. Creation happens via the admin action; deletion is not allowed.
"""

from __future__ import annotations

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from koalixcrm.core.models.pdf_export_process import PDFExportProcess
from koalixcrm.core.serializers.pdf_export_process_serializer import (
    PDFExportProcessJSONSerializer,
)
from koalixcrm.shared.permissions import ModelPermissionsWithListView


class PDFExportProcessViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = PDFExportProcess.objects.all()
    serializer_class = PDFExportProcessJSONSerializer
    permission_classes = [IsAuthenticated, ModelPermissionsWithListView]
    http_method_names = ["get", "patch", "head", "options"]
