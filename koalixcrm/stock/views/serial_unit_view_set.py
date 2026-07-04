# -*- coding: utf-8 -*-
"""
SerialUnitViewSet for koalixcrm stock

ADR-0015: the lifecycle history read-only endpoints (`history`,
`as-built`, `installed-components`, `holder-timeline`, `location-timeline`)
delegate to `services/lifecycle_history.py` — pure projections over the
immutable `StockMovement` log, never writing anything.
"""
from __future__ import annotations

from rest_framework.decorators import action
from rest_framework.response import Response

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.serial_unit import SerialUnit
from koalixcrm.stock.serializers.serial_unit_serializer import SerialUnitJSONSerializer
from koalixcrm.stock.serializers.stock_movement_serializer import StockMovementJSONSerializer
from koalixcrm.stock.services import lifecycle_history


class SerialUnitViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = SerialUnitJSONSerializer
    queryset = SerialUnit.objects.all()

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """ADR-0015 §Vollständige Einheitenhistorie."""
        serial_unit = self.get_object()
        movements = lifecycle_history.full_history(serial_unit)
        return Response(StockMovementJSONSerializer(movements, many=True).data)

    @action(detail=True, methods=['get'], url_path='as-built')
    def as_built(self, request, pk=None):
        """ADR-0015 §As-Built-BOM."""
        serial_unit = self.get_object()
        movements = lifecycle_history.as_built_bom(serial_unit)
        return Response(StockMovementJSONSerializer(movements, many=True).data)

    @action(detail=True, methods=['get'], url_path='installed-components')
    def installed_components(self, request, pk=None):
        """ADR-0015 §Aktuell installierte Komponenten."""
        serial_unit = self.get_object()
        components = lifecycle_history.installed_components(serial_unit)
        return Response(SerialUnitJSONSerializer(components, many=True).data)

    @action(detail=True, methods=['get'], url_path='holder-timeline')
    def holder_timeline(self, request, pk=None):
        """ADR-0015 §Halter-Zeitleiste (`who_held_it_when`), Amendment
        2026-05-04 OQ-0014."""
        serial_unit = self.get_object()
        windows = lifecycle_history.who_held_it_when(serial_unit)
        return Response([
            {
                "holder_party": window.holder_party_id,
                "from": window.holder_from,
                "to": window.holder_to,
            }
            for window in windows
        ])

    @action(detail=True, methods=['get'], url_path='location-timeline')
    def location_timeline(self, request, pk=None):
        """ADR-0015 §Standort-Zeitleiste (`where_was_it_when`), Amendment
        2026-05-04 (UC-0008/0009/0010)."""
        serial_unit = self.get_object()
        windows = lifecycle_history.where_was_it_when(serial_unit)
        return Response([
            {
                "location": window.location_id,
                "from": window.location_from,
                "to": window.location_to,
            }
            for window in windows
        ])
