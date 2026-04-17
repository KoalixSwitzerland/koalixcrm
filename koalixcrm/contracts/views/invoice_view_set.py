# -*- coding: utf-8 -*-
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.serializers.invoice_serializer import InvoiceJSONSerializer
from koalixcrm.contracts.serializers.nested_commercial_document import (
    InvoiceNestedSerializer,
)
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class InvoiceViewSet(NestedDetailMixin, BaseModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceJSONSerializer
    nested_serializer_class = InvoiceNestedSerializer
