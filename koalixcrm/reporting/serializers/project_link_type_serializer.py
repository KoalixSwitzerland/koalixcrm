# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.reporting.models.project_link_type import ProjectLinkType


class ProjectLinkTypeJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLinkType
        fields = '__all__'
