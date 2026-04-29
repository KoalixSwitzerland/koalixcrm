# -*- coding: utf-8 -*-
"""
Read-only DocumentTemplate ViewSet + presigned-URL detail actions.

The PDF worker calls:

* ``GET /api/document_templates/{id}/`` to read metadata + sub-resource hrefs,
* ``GET /api/document_templates/{id}/xsl/`` → 302 redirect to a short-lived
  presigned S3 URL for the XSL-FO stylesheet (same for ``fop-config`` and
  ``logo``). Missing optional assets return ``404``.
"""
from __future__ import annotations

from typing import Any

from django.db.models import QuerySet
from django.db.models.fields.files import FieldFile
from django.http import HttpResponseRedirect
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer

from koalixcrm.djangoUserExtension.models.document_template import DocumentTemplate
from koalixcrm.djangoUserExtension.serializers.document_template_serializer import (
    DocumentTemplateJSONSerializer,
)
from koalixcrm.shared.permissions import ModelPermissionsWithListView
from koalixcrm_utils.presigned_urls import presigned_get_url_for_field


class DocumentTemplateViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateJSONSerializer
    permission_classes = [IsAuthenticated, ModelPermissionsWithListView]
    http_method_names = ["get", "head", "options"]

    def get_queryset(self) -> QuerySet[DocumentTemplate]:
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return DocumentTemplate.objects.all()
        if active is None:
            return DocumentTemplate.objects.none()
        return DocumentTemplate.objects.filter(workspace=active)

    def perform_create(self, serializer: BaseSerializer) -> None:
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)

    def _redirect_to_field(self, field_file: FieldFile, asset_name: str) -> HttpResponseRedirect:
        if not field_file:
            raise NotFound(detail=f"{asset_name} not set on this template")
        url = presigned_get_url_for_field(field_file)
        return HttpResponseRedirect(url)

    @action(detail=True, methods=["get"], url_path="xsl", url_name="xsl")
    def xsl(self, request: Any, pk: int | None = None, **kwargs: Any) -> HttpResponseRedirect:
        return self._redirect_to_field(self.get_object().xsl_file, "xsl_file")

    @action(detail=True, methods=["get"], url_path="fop-config", url_name="fop-config")
    def fop_config(self, request: Any, pk: int | None = None, **kwargs: Any) -> HttpResponseRedirect:
        return self._redirect_to_field(
            self.get_object().fop_config_file, "fop_config_file"
        )

    @action(detail=True, methods=["get"], url_path="logo", url_name="logo")
    def logo(self, request: Any, pk: int | None = None, **kwargs: Any) -> HttpResponseRedirect:
        return self._redirect_to_field(self.get_object().logo, "logo")
