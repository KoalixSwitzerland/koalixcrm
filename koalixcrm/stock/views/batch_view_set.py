# -*- coding: utf-8 -*-
"""
BatchViewSet for koalixcrm stock
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.batch import Batch
from koalixcrm.stock.serializers.batch_serializer import BatchJSONSerializer


class BatchViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = BatchJSONSerializer
    queryset = Batch.objects.all()
