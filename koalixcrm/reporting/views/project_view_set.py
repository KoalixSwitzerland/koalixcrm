"""
ProjectViewSet for koalixcrm reporting
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.project import Project
from ..serializers.project_serializer import ProjectJSONSerializer


class ProjectViewSet(BaseModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectJSONSerializer
