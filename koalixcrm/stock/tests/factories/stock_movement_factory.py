# -*- coding: utf-8 -*-
import uuid

import factory
from django.utils import timezone

from koalixcrm.stock.models.choices import BusinessStep, EventType
from koalixcrm.stock.models.stock_movement import StockMovement
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory
from koalixcrm.stock.tests.factories.location_factory import StandardLocationFactory


class StandardStockMovementFactory(factory.django.DjangoModelFactory):
    """Builds StockMovement rows directly (bypassing the posting service) —
    only for tests that need a pre-existing log row (e.g. immutability,
    retention) without needing OnHandRecord/StockBalance side effects."""

    class Meta:
        model = StockMovement

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    event_type = EventType.OBJECT_EVENT
    business_step = BusinessStep.RECEIVING
    occurred_at = factory.LazyFunction(timezone.now)
    variant = factory.SubFactory(StandardProductVariantFactory)
    product = factory.LazyAttribute(lambda o: o.variant.product)
    destination_location = factory.SubFactory(StandardLocationFactory)
    qty = "10.0000"
    uom = factory.SubFactory(StandardUnitFactory)
    idempotency_key = factory.LazyFunction(uuid.uuid4)
