# -*- coding: utf-8 -*-
from koalixcrm.reporting.models.resource import Resource
from koalixcrm.reporting.serializers.resource_serializer import ResourceJSONSerializer
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class ResourceViewSet(BaseModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceJSONSerializer
