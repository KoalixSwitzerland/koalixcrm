# -*- coding: utf-8 -*-
from rest_framework import viewsets
from koalixcrm.crm.reporting.task import Task, TaskJSONSerializer
from koalixcrm.crm.reporting.taskstatus import TaskStatus, TaskStatusJSONSerializer
from koalixcrm.crm.documents.contract import Contract, ContractJSONSerializer
from rest_framework.response import Response


class TaskAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Task.objects.all()
    serializer_class = TaskJSONSerializer

    def listed(self, request, kwargs):
        projects = kwargs['project']
        queryset = Task.objects.filter(project=projects)
        serializer = TaskJSONSerializer(queryset)
        return Response(serializer.data)


class ContractAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Contract.objects.all()
    serializer_class = ContractJSONSerializer


class TaskStatusAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusJSONSerializer