# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.accounting.models import AccountingPeriod
from koalixcrm.accounting.serializers.accounting_period_serializer import AccountingPeriodJSONSerializer


class AccountingPeriodViewSet(BaseModelViewSet):
    queryset = AccountingPeriod.objects.all()
    serializer_class = AccountingPeriodJSONSerializer
