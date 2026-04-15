# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.project_link_type import ProjectLinkType
from koalixcrm.reporting.serializers.project_link_type_serializer import ProjectLinkTypeJSONSerializer


class ProjectLinkTypeViewSet(BaseModelViewSet):
    queryset = ProjectLinkType.objects.all()
    serializer_class = ProjectLinkTypeJSONSerializer
