# -*- coding: utf-8 -*-
import factory

from koalixcrm.stock.models.choices import OwnerType
from koalixcrm.stock.models.on_hand_record import OnHandRecord
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_variant_factory import StandardProductVariantFactory
from tests.factories.stock.location_factory import StandardLocationFactory


class StandardOnHandRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OnHandRecord

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    variant = factory.SubFactory(StandardProductVariantFactory)
    location = factory.SubFactory(StandardLocationFactory)
    owner_type = OwnerType.OWN
    qty_on_hand = "10.0000"
    uom = factory.SubFactory(StandardUnitFactory)
