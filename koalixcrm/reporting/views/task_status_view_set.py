"""
TaskStatusViewSet for koalixcrm reporting
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.task_status import TaskStatus
from ..serializers.task_status_serializer import TaskStatusJSONSerializer


class TaskStatusViewSet(BaseModelViewSet):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusJSONSerializer
