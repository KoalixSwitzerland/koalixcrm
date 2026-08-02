# -*- coding: utf-8 -*-
import factory
from django.utils import timezone

from koalixcrm.stock.models.choices import ReservationLifecycleStatus
from koalixcrm.stock.models.rental_assignment import RentalAssignment
from koalixcrm.contacts.tests.factories.contact_factory import StandardContactFactory
from koalixcrm.stock.tests.factories.stock_reservation_factory import RentalStockReservationFactory


class StandardRentalAssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RentalAssignment

    reservation = factory.SubFactory(
        RentalStockReservationFactory, status=ReservationLifecycleStatus.FULFILLED
    )
    workspace = factory.LazyAttribute(lambda o: o.reservation.workspace)
    serial_unit = factory.LazyAttribute(lambda o: o.reservation.serial_unit)
    party = factory.SubFactory(StandardContactFactory)
    rental_start = factory.LazyFunction(timezone.now)
