# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.work import Work
from koalixcrm.reporting.serializers.work_serializer import WorkJSONSerializer


class WorkViewSet(BaseModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkJSONSerializer
