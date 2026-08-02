# -*- coding: utf-8 -*-
"""ADR-0010 Amendment 2026-05-04 (OQ-0011): schema-only serializers for
`GET .../variants/{id}/serial-units/availability/`.

The view hand-builds its payload from `services/availability.free_windows`
rather than going through a serializer, so these exist purely to give
drf-spectacular a shape to publish. Keep them in sync with the view.
"""
from __future__ import annotations

from rest_framework import serializers

# `from` is a Python keyword, so the window bounds cannot be declared as
# ordinary class attributes. DRF's SerializerMetaclass collects declared
# fields out of the class namespace dict, which `type()` lets us populate
# with the wire names the view actually emits.
FreeWindowSerializer = type(
    'FreeWindowSerializer',
    (serializers.Serializer,),
    {
        '__doc__': "A contiguous interval in which the serial unit is unassigned.",
        'from': serializers.DateTimeField(help_text="Start of the free window (ISO-8601)."),
        'to': serializers.DateTimeField(help_text="End of the free window (ISO-8601)."),
    },
)


class SerialUnitAvailabilitySerializer(serializers.Serializer):
    """One entry per serial unit of the requested variant."""

    serial_unit = serializers.IntegerField(help_text="SerialUnit primary key.")
    serial_number = serializers.CharField(help_text="Human-readable serial number.")
    free = serializers.BooleanField(
        help_text="True when the unit is free across the entire requested window.",
    )
    free_windows = FreeWindowSerializer(many=True)
