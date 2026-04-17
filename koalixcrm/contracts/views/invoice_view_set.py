# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.serializers.invoice_serializer import InvoiceJSONSerializer


class InvoiceViewSet(BaseModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceJSONSerializer
