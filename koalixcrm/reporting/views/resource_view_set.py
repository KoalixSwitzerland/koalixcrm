# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.reporting.models.resource import Resource
from koalixcrm.reporting.serializers.resource_serializer import ResourceJSONSerializer
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ResourceViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceJSONSerializer
