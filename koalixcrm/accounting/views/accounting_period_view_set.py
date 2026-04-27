# -*- coding: utf-8 -*-
from rest_framework.decorators import action
from rest_framework.response import Response

from koalixcrm.accounting.models import AccountingPeriod
from koalixcrm.accounting.serializers.accounting_period_serializer import (
    AccountingPeriodJSONSerializer,
    AccountingPeriodReportSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class AccountingPeriodViewSet(BaseModelViewSet):
    queryset = AccountingPeriod.objects.all()
    serializer_class = AccountingPeriodJSONSerializer

    @action(detail=True, methods=['get'], url_path='report-data')
    def report_data(self, request, pk=None, **kwargs):
        """Self-contained snapshot for FOP balancesheet / profitlossstatement:
        period header + four overall aggregates + per-account sums for every
        account, in a single payload.
        """
        period = self.get_object()
        serializer = AccountingPeriodReportSerializer(period)
        return Response(serializer.data)
