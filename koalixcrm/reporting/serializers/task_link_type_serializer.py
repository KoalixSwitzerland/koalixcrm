# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.reporting.models.task_link_type import TaskLinkType


class TaskLinkTypeJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLinkType
        fields = '__all__'
