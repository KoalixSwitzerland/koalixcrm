# -*- coding: utf-8 -*-
from rest_framework import viewsets
from koalixcrm.crm.reporting.task import Task, TaskJSONSerializer
from koalixcrm.crm.reporting.taskstatus import TaskStatus, TaskStatusJSONSerializer
from koalixcrm.crm.documents.contract import Contract, ContractJSONSerializer



class TaskAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Task.objects.all()
    serializer_class = TaskJSONSerializer
    filter_fields = ('project',)


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