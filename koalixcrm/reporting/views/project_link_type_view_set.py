# -*- coding: utf-8 -*-
from koalixcrm.reporting.models.project_link_type import ProjectLinkType
from koalixcrm.reporting.serializers.project_link_type_serializer import (
    ProjectLinkTypeJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class ProjectLinkTypeViewSet(BaseModelViewSet):
    queryset = ProjectLinkType.objects.all()
    serializer_class = ProjectLinkTypeJSONSerializer
