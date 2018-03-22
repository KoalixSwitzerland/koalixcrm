# -*- coding: utf-8 -*-
from rest_framework import viewsets
from koalixcrm.crm.reporting.task import Task, TaskJSONSerializer
from rest_framework.response import Response


class TaskAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Task.objects.all()
    serializer_class = TaskJSONSerializer

    def list(self, request, kwargs):
        projects = kwargs['project']
        queryset = Task.objects.filter(project=projects)
        serializer = TaskJSONSerializer(queryset)
        return Response(serializer.data)



