# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.quote import Quote
from koalixcrm.contracts.serializers.quote_serializer import QuoteJSONSerializer


class QuoteViewSet(BaseModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteJSONSerializer
