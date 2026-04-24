# -*- coding: utf-8 -*-
import datetime

from rest_framework import status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.human_resource import HumanResource
from koalixcrm.reporting.serializers.human_resource_serializer import (
    HumanResourceJSONSerializer,
)
from koalixcrm.reporting.serializers.human_resource_report_serializer import (
    HumanResourceWorkReportSerializer,
    WorkReportBuilder,
)


class HumanResourceViewSet(BaseModelViewSet):
    queryset = HumanResource.objects.all()
    serializer_class = HumanResourceJSONSerializer

    @action(detail=True, methods=['get'], url_path='work-report-data')
    def work_report_data(self, request, pk=None, **kwargs):
        """Self-contained snapshot for the work_report XSL. Pass
        ``?range_from=YYYY-MM-DD&range_to=YYYY-MM-DD`` (defaults: 60 days
        back to today, mirroring the legacy serialize_to_xml defaults).
        """
        hr = self.get_object()
        try:
            date_from = self._parse('range_from', request,
                                    default=datetime.date.today() - datetime.timedelta(days=60))
            date_to = self._parse('range_to', request, default=datetime.date.today())
        except ValueError as e:
            return Response({'detail': str(e)},
                            status=http_status.HTTP_400_BAD_REQUEST)
        if date_from > date_to:
            return Response({'detail': "range_from must be <= range_to"},
                            status=http_status.HTTP_400_BAD_REQUEST)
        payload = WorkReportBuilder(hr, date_from, date_to).build()
        return Response(HumanResourceWorkReportSerializer(payload).data)

    @staticmethod
    def _parse(name, request, default):
        raw = request.query_params.get(name)
        if not raw:
            return default
        try:
            return datetime.date.fromisoformat(raw)
        except ValueError:
            raise ValueError(f"{name} must be YYYY-MM-DD, got {raw!r}")
