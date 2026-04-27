"""
TaskViewSet for koalixcrm reporting
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.task import Task
from ..serializers.task_serializer import TaskJSONSerializer


class TaskViewSet(BaseModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskJSONSerializer
    filterset_fields = ['project']
