# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.accounting.models import Booking
from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.accounting.tests.factories.account_factory import (
    OpenInterestAccountFactory,
    StandardAccountFactory,
)
from koalixcrm.accounting.tests.factories.accounting_period_factory import (
    StandardAccountingPeriodFactory,
)
from koalixcrm.contacts.tests.factories.user_factory import StaffUserFactory


class StandardBookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    from_account = factory.SubFactory(StandardAccountFactory)
    to_account = factory.SubFactory(OpenInterestAccountFactory)
    amount = "100.00"
    description = "This is a test booking"
    booking_reference = None
    booking_date = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    accounting_period = factory.SubFactory(StandardAccountingPeriodFactory)
    staff = factory.SubFactory(StaffUserFactory)
    last_modified_by = factory.SubFactory(StaffUserFactory)
