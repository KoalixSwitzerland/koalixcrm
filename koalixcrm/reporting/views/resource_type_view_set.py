# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.resource_type import ResourceType
from koalixcrm.reporting.serializers.resource_type_serializer import ResourceTypeJSONSerializer


class ResourceTypeViewSet(BaseModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeJSONSerializer
