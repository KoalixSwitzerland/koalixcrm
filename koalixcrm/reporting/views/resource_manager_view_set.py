# -*- coding: utf-8 -*-
from koalixcrm.reporting.models.resource_manager import ResourceManager
from koalixcrm.reporting.serializers.resource_manager_serializer import (
    ResourceManagerJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class ResourceManagerViewSet(BaseModelViewSet):
    queryset = ResourceManager.objects.all()
    serializer_class = ResourceManagerJSONSerializer
