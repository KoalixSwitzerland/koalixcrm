"""
ProjectStatusViewSet for koalixcrm reporting
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.project_status import ProjectStatus
from ..serializers.project_status_serializer import ProjectStatusJSONSerializer


class ProjectStatusViewSet(BaseModelViewSet):
    queryset = ProjectStatus.objects.all()
    serializer_class = ProjectStatusJSONSerializer
