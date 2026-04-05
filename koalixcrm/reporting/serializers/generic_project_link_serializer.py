# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.reporting.models.generic_project_link import GenericProjectLink


class GenericProjectLinkJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericProjectLink
        fields = '__all__'
