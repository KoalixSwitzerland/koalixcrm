# -*- coding: utf-8 -*-
"""`GET .../variants/{id}/serial-units/availability/?start=&end=` (ADR-0010
Amendment 2026-05-04 OQ-0011, rekeyed to `ProductVariant` by Amendment
2026-07-04). The sole authorized interface for time-window availability
queries; the frontend calls this before saving a rental offer position."""
from __future__ import annotations

from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from koalixcrm.products.models.product_variant import ProductVariant
from koalixcrm.stock.services.availability import free_windows


class SerialUnitAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, variant_id, workspace_id=None):
        start = parse_datetime(request.query_params.get('start', ''))
        end = parse_datetime(request.query_params.get('end', ''))
        if start is None or end is None:
            return Response(
                {"detail": "Query params 'start' and 'end' are required ISO-8601 datetimes."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            variant = ProductVariant.objects.get(pk=variant_id)
        except ProductVariant.DoesNotExist:
            return Response({"detail": "ProductVariant not found."}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_superuser:
            active_workspace = getattr(request, 'active_workspace', None)
            if active_workspace is None or variant.workspace_id != active_workspace.id:
                return Response({"detail": "ProductVariant not found."}, status=status.HTTP_404_NOT_FOUND)

        results = free_windows(variant, start, end)
        payload = [
            {
                "serial_unit": unit.pk,
                "serial_number": unit.serial_number,
                "free": bool(windows) and windows == [(start, end)],
                "free_windows": [
                    {"from": window_start.isoformat(), "to": window_end.isoformat()}
                    for window_start, window_end in windows
                ],
            }
            for unit, windows in results
        ]
        return Response(payload)
