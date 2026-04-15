# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.reporting_period_status import ReportingPeriodStatus
from koalixcrm.reporting.serializers.reporting_period_status_serializer import ReportingPeriodStatusJSONSerializer


class ReportingPeriodStatusViewSet(BaseModelViewSet):
    queryset = ReportingPeriodStatus.objects.all()
    serializer_class = ReportingPeriodStatusJSONSerializer
