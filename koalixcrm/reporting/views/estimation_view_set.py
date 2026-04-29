# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.reporting.models.estimation import Estimation
from koalixcrm.reporting.serializers.estimation_serializer import (
    EstimationJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class EstimationViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = Estimation.objects.all()
    serializer_class = EstimationJSONSerializer
