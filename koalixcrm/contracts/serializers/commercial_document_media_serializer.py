# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.contracts.models.commercial_document_media import (
    CommercialDocumentS3Media,
)


class CommercialDocumentS3MediaJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialDocumentS3Media
        fields = (
            "id",
            "commercial_document",
            "s3_url",
            "status",
            "media_type",
            "created_by",
            "created_at",
            "last_updated_at",
        )
        read_only_fields = ("id", "created_at", "last_updated_at")
