# -*- coding: utf-8 -*-
from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.contracts.serializers.nested_commercial_document import (
    QuotationNestedSerializer,
)
from koalixcrm.contracts.serializers.quotation_serializer import QuotationJSONSerializer
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class QuotationViewSet(NestedDetailMixin, BaseModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationJSONSerializer
    nested_serializer_class = QuotationNestedSerializer
