# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.serializers.invoice_serializer import InvoiceJSONSerializer
from koalixcrm.contracts.serializers.nested_commercial_document import (
    InvoiceNestedSerializer,
)
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class InvoiceViewSet(WorkspaceScopedViewSetMixin, NestedDetailMixin, BaseModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceJSONSerializer
    nested_serializer_class = InvoiceNestedSerializer
