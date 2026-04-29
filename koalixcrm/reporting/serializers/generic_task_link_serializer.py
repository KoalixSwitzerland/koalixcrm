# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.reporting.models.generic_task_link import GenericTaskLink


class GenericTaskLinkJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericTaskLink
        fields = '__all__'
