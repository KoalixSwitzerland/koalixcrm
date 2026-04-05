# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.agreement_status import AgreementStatus
from koalixcrm.reporting.serializers.agreement_status_serializer import AgreementStatusJSONSerializer


class AgreementStatusViewSet(BaseModelViewSet):
    queryset = AgreementStatus.objects.all()
    serializer_class = AgreementStatusJSONSerializer
