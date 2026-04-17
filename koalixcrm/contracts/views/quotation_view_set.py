# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.contracts.serializers.quotation_serializer import QuotationJSONSerializer


class QuotationViewSet(BaseModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationJSONSerializer
