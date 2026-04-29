# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.reporting.models.resource_type import ResourceType
from koalixcrm.reporting.serializers.resource_type_serializer import (
    ResourceTypeJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class ResourceTypeViewSet(BaseModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeJSONSerializer
