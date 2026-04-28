# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.reporting.models.agreement_status import AgreementStatus
from koalixcrm.reporting.serializers.agreement_status_serializer import (
    AgreementStatusJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class AgreementStatusViewSet(BaseModelViewSet):
    queryset = AgreementStatus.objects.all()
    serializer_class = AgreementStatusJSONSerializer
