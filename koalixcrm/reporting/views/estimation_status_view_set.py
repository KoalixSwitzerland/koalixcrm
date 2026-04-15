# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.estimation_status import EstimationStatus
from koalixcrm.reporting.serializers.estimation_status_serializer import EstimationStatusJSONSerializer


class EstimationStatusViewSet(BaseModelViewSet):
    queryset = EstimationStatus.objects.all()
    serializer_class = EstimationStatusJSONSerializer
