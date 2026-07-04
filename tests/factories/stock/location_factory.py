# -*- coding: utf-8 -*-
import factory

from koalixcrm.stock.models.choices import LocationType
from koalixcrm.stock.models.location import Location
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory


class StandardLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    location_type = LocationType.WAREHOUSE
    code = factory.Sequence(lambda n: f"LOC-{n}")
    name = "Main Warehouse"
    is_active = True
