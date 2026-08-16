# -*- coding: utf-8 -*-
import factory

from koalixcrm.stock.models.retention_policy import RetentionPolicy
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory


class StandardRetentionPolicyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RetentionPolicy
        django_get_or_create = ('workspace',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    serial_unit_retention_floor_days = None
