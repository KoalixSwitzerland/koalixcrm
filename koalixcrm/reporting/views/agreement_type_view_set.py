# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.reporting.models.agreement_type import AgreementType
from koalixcrm.reporting.serializers.agreement_type_serializer import (
    AgreementTypeJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class AgreementTypeViewSet(BaseModelViewSet):
    queryset = AgreementType.objects.all()
    serializer_class = AgreementTypeJSONSerializer
