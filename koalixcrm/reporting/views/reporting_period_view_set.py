# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from rest_framework.decorators import action
from rest_framework.response import Response

from koalixcrm.reporting.models.reporting_period import ReportingPeriod
from koalixcrm.reporting.serializers.project_report_serializer import (
    ProjectReportSerializer,
)
from koalixcrm.reporting.serializers.reporting_period_serializer import (
    ReportingPeriodJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class ReportingPeriodViewSet(BaseModelViewSet):
    queryset = ReportingPeriod.objects.all()
    serializer_class = ReportingPeriodJSONSerializer

    @action(detail=True, methods=['get'], url_path='report-data')
    def report_data(self, request: Any, pk: Any = None, **kwargs: Any) -> Response:
        """A reporting-period report is just a period-scoped project report —
        the legacy ``ReportingPeriod.serialize_to_xml`` delegated to
        ``Project.serialize_to_xml(reporting_period=self)``. We do the same
        here so the Java side has a single XSL → builder mapping for both
        the project_report XSL.
        """
        period = self.get_object()
        serializer = ProjectReportSerializer(
            period.project,
            context={'reporting_period': period, 'request': request},
        )
        return Response(serializer.data)
