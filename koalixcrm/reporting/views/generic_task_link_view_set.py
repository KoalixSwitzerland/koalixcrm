# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.generic_task_link import GenericTaskLink
from koalixcrm.reporting.serializers.generic_task_link_serializer import GenericTaskLinkJSONSerializer


class GenericTaskLinkViewSet(BaseModelViewSet):
    queryset = GenericTaskLink.objects.all()
    serializer_class = GenericTaskLinkJSONSerializer
