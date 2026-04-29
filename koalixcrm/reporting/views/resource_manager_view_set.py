# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.reporting.models.resource_manager import ResourceManager
from koalixcrm.reporting.serializers.resource_manager_serializer import (
    ResourceManagerJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ResourceManagerViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = ResourceManager.objects.all()
    serializer_class = ResourceManagerJSONSerializer
