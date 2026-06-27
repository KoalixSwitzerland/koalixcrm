# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.contracts.models.commercial_document_media import (
    CommercialDocumentMedia,
)


class CommercialDocumentMediaJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialDocumentMedia
        fields = (
            "id",
            "commercial_document",
            "s3_url",
            "s3_key",
            "status",
            "media_type",
            "created_by",
            "created_at",
            "last_updated_at",
        )
        read_only_fields = ("id", "created_at", "last_updated_at")
