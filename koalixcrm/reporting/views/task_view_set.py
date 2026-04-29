"""
TaskViewSet for koalixcrm reporting
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin

from ..models.task import Task
from ..serializers.task_serializer import TaskJSONSerializer


class TaskViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskJSONSerializer
    filterset_fields = ['project']
