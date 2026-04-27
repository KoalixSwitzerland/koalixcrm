# -*- coding: utf-8 -*-
from koalixcrm.reporting.models.estimation_status import EstimationStatus
from koalixcrm.reporting.serializers.estimation_status_serializer import (
    EstimationStatusJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class EstimationStatusViewSet(BaseModelViewSet):
    queryset = EstimationStatus.objects.all()
    serializer_class = EstimationStatusJSONSerializer
