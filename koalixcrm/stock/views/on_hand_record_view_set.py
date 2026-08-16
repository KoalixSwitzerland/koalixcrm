# -*- coding: utf-8 -*-
"""
OnHandRecordViewSet for koalixcrm stock
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.on_hand_record import OnHandRecord
from koalixcrm.stock.serializers.on_hand_record_serializer import OnHandRecordJSONSerializer


class OnHandRecordViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = OnHandRecordJSONSerializer
    queryset = OnHandRecord.objects.all()
