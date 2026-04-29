# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.reporting.models.work import Work
from koalixcrm.reporting.serializers.work_serializer import WorkJSONSerializer
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class WorkViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkJSONSerializer
