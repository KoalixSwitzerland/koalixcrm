# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.contracts.serializers.nested_commercial_document import (
    QuotationNestedSerializer,
)
from koalixcrm.contracts.serializers.quotation_serializer import QuotationJSONSerializer
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class QuotationViewSet(WorkspaceScopedViewSetMixin, NestedDetailMixin, BaseModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationJSONSerializer
    nested_serializer_class = QuotationNestedSerializer
