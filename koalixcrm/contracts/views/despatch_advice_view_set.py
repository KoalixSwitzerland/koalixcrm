# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.contracts.models.despatch_advice import DespatchAdvice
from koalixcrm.contracts.serializers.despatch_advice_serializer import (
    DespatchAdviceJSONSerializer,
)
from koalixcrm.contracts.serializers.nested_commercial_document import (
    DespatchAdviceNestedSerializer,
)
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class DespatchAdviceViewSet(WorkspaceScopedViewSetMixin, NestedDetailMixin, BaseModelViewSet):
    queryset = DespatchAdvice.objects.all()
    serializer_class = DespatchAdviceJSONSerializer
    nested_serializer_class = DespatchAdviceNestedSerializer
