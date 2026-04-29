# -*- coding: utf-8 -*-
"""
Flat JSON serializer for :class:`DocumentTemplate`.

Used by the PDF worker: returns template metadata plus ``*_href`` sub-resource
URLs that 302-redirect to short-lived presigned S3 download URLs. The binary
assets themselves are never embedded in the JSON payload.
"""
from __future__ import annotations

from rest_framework import serializers
from rest_framework.reverse import reverse

from koalixcrm.djangoUserExtension.models.document_template import DocumentTemplate


class DocumentTemplateJSONSerializer(serializers.ModelSerializer):
    xsl_href = serializers.SerializerMethodField()
    fop_config_href = serializers.SerializerMethodField()
    logo_href = serializers.SerializerMethodField()

    class Meta:
        model = DocumentTemplate
        fields = ("id", "title", "xsl_href", "fop_config_href", "logo_href")

    def _detail_url(self, instance: DocumentTemplate, action: str) -> str:
        request = self.context.get("request")
        # Under CR-002 the basename is `document-template` (kebab-case) and the
        # URL carries a `workspace_id` path arg. Pull it from the resolver
        # match so the reverse() round-trips regardless of which workspace
        # the request came in under.
        workspace_id = None
        if request is not None and getattr(request, "resolver_match", None) is not None:
            workspace_id = request.resolver_match.kwargs.get("workspace_id")
        kwargs = {"pk": instance.pk}
        if workspace_id is not None:
            kwargs["workspace_id"] = workspace_id
        return reverse(
            f"document-template-{action}",
            kwargs=kwargs,
            request=request,
        )

    def get_xsl_href(self, instance: DocumentTemplate) -> str:
        return self._detail_url(instance, "xsl")

    def get_fop_config_href(self, instance: DocumentTemplate) -> str:
        return self._detail_url(instance, "fop-config")

    def get_logo_href(self, instance: DocumentTemplate) -> str:
        return self._detail_url(instance, "logo")
