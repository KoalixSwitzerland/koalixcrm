# -*- coding: utf-8 -*-
import factory

from koalixcrm.stock.models.choices import HandlingUnitType
from koalixcrm.stock.models.handling_unit import HandlingUnit
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.stock.tests.factories.location_factory import StandardLocationFactory


class StandardHandlingUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HandlingUnit

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    sscc = factory.Sequence(lambda n: str(100000000000000000 + n)[-18:])
    location = factory.SubFactory(StandardLocationFactory)
    hu_type = HandlingUnitType.PALLET
    is_open = True
