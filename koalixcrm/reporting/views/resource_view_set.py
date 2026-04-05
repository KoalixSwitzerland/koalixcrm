# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.resource import Resource
from koalixcrm.reporting.serializers.resource_serializer import ResourceJSONSerializer


class ResourceViewSet(BaseModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceJSONSerializer
