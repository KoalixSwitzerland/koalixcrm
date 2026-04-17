# -*- coding: utf-8 -*-
"""
Flat JSON serializer for :class:`DocumentTemplate`.

Used by the PDF worker: returns template metadata plus ``*_href`` sub-resource
URLs that 302-redirect to short-lived presigned S3 download URLs. The binary
assets themselves are never embedded in the JSON payload.
"""
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

    def _detail_url(self, instance, action):
        request = self.context.get("request")
        return reverse(
            f"documenttemplate-{action}",
            kwargs={"pk": instance.pk},
            request=request,
        )

    def get_xsl_href(self, instance):
        return self._detail_url(instance, "xsl")

    def get_fop_config_href(self, instance):
        return self._detail_url(instance, "fop-config")

    def get_logo_href(self, instance):
        return self._detail_url(instance, "logo")
