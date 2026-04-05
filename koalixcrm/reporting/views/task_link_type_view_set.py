# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.task_link_type import TaskLinkType
from koalixcrm.reporting.serializers.task_link_type_serializer import TaskLinkTypeJSONSerializer


class TaskLinkTypeViewSet(BaseModelViewSet):
    queryset = TaskLinkType.objects.all()
    serializer_class = TaskLinkTypeJSONSerializer
