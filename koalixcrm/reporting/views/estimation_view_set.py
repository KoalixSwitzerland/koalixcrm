# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.estimation import Estimation
from koalixcrm.reporting.serializers.estimation_serializer import EstimationJSONSerializer


class EstimationViewSet(BaseModelViewSet):
    queryset = Estimation.objects.all()
    serializer_class = EstimationJSONSerializer
