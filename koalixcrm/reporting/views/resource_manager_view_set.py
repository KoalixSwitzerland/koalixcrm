# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.resource_manager import ResourceManager
from koalixcrm.reporting.serializers.resource_manager_serializer import ResourceManagerJSONSerializer


class ResourceManagerViewSet(BaseModelViewSet):
    queryset = ResourceManager.objects.all()
    serializer_class = ResourceManagerJSONSerializer
