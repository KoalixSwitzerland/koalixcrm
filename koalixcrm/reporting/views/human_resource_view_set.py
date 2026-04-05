# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.human_resource import HumanResource
from koalixcrm.reporting.serializers.human_resource_serializer import HumanResourceJSONSerializer


class HumanResourceViewSet(BaseModelViewSet):
    queryset = HumanResource.objects.all()
    serializer_class = HumanResourceJSONSerializer
