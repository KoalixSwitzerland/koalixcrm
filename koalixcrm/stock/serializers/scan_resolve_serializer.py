# -*- coding: utf-8 -*-
"""ADR-0016: schema-only serializers for `POST .../scan/resolve/`.

The view hand-builds its payloads from `services/scan_resolve.ScanMatch`
rather than going through a serializer, so these exist purely to give
drf-spectacular a shape to publish. Keep them in sync with
`ScanMatch.as_dict()` and the view's error branches.
"""
from __future__ import annotations

from rest_framework import serializers


class ScanResolveRequestSerializer(serializers.Serializer):
    code = serializers.CharField(
        help_text="Raw scanned code: a GS1 element string or a free-text identifier.",
    )


class ScanMatchSerializer(serializers.Serializer):
    """Mirrors `scan_resolve.ScanMatch.as_dict()`."""

    kind = serializers.ChoiceField(
        choices=['serial_unit', 'handling_unit', 'location', 'product_variant'],
        help_text="Which entity the code resolved to.",
    )
    id = serializers.IntegerField(help_text="Primary key of the resolved entity.")
    matched_field = serializers.CharField(
        help_text="The identifier field that produced the match, e.g. 'gtin' or 'sku'.",
    )


class ScanResolveConflictSerializer(serializers.Serializer):
    """409: free-text matched more than one entity, so the caller must choose."""

    detail = serializers.CharField()
    candidates = ScanMatchSerializer(many=True)


class DetailSerializer(serializers.Serializer):
    """The bare `{"detail": ...}` body used by the 400 and 404 branches."""

    detail = serializers.CharField()
