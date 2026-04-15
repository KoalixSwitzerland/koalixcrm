# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.reporting_period import ReportingPeriod
from koalixcrm.reporting.serializers.reporting_period_serializer import ReportingPeriodJSONSerializer


class ReportingPeriodViewSet(BaseModelViewSet):
    queryset = ReportingPeriod.objects.all()
    serializer_class = ReportingPeriodJSONSerializer
