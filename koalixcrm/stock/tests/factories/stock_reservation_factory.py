# -*- coding: utf-8 -*-
import datetime

import factory
from django.utils import timezone

from koalixcrm.stock.models.choices import ReservationKind
from koalixcrm.stock.models.stock_reservation import StockReservation
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory
from koalixcrm.stock.tests.factories.serial_unit_factory import StandardSerialUnitFactory


class StandardStockReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockReservation

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    variant = factory.SubFactory(StandardProductVariantFactory)
    kind = ReservationKind.SALE
    qty_reserved = "1.0000"
    uom = factory.SubFactory(StandardUnitFactory)


class RentalStockReservationFactory(StandardStockReservationFactory):
    kind = ReservationKind.RENTAL
    qty_reserved = None
    serial_unit = factory.SubFactory(StandardSerialUnitFactory)
    rental_start = factory.LazyFunction(timezone.now)
    rental_end = factory.LazyAttribute(lambda o: o.rental_start + datetime.timedelta(days=7))
