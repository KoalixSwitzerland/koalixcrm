# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.core.models.pdf_export_process import PDFExportProcess


class PDFExportProcessJSONSerializer(serializers.ModelSerializer):
    """
    Read/update serializer for :class:`PDFExportProcess`.

    The worker PATCHes ``status``, ``result_url`` and ``error_message`` as it
    progresses. All other fields are read-only — they are set by the Django
    producer when the job is enqueued.
    """

    class Meta:
        model = PDFExportProcess
        fields = (
            "id",
            "source_model",
            "source_id",
            "template_set",
            "triggered_by",
            "status",
            "result_url",
            "error_message",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "source_model",
            "source_id",
            "template_set",
            "triggered_by",
            "created_at",
            "updated_at",
        )
