# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.despatch_advice import DespatchAdvice
from koalixcrm.contracts.serializers.despatch_advice_serializer import DespatchAdviceJSONSerializer


class DespatchAdviceViewSet(BaseModelViewSet):
    queryset = DespatchAdvice.objects.all()
    serializer_class = DespatchAdviceJSONSerializer
