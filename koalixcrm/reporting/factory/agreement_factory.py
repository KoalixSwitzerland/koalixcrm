# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.reporting.models.agreement import Agreement
from koalixcrm.reporting.factory.resource_factory import StandardResourceFactory
from koalixcrm.reporting.factory.human_resource_factory import StandardHumanResourceFactory
from koalixcrm.reporting.factory.task_factory import StandardTaskFactory
from koalixcrm.settings.factory.unit_factory import StandardUnitFactory
from koalixcrm.reporting.factory.resource_price_factory import StandardResourcePriceFactory
from koalixcrm.reporting.factory.agreement_type_factory import StandardAgreementTypeFactory
from koalixcrm.reporting.factory.agreement_status_factory import AgreedAgreementStatusFactory
from koalixcrm.global_support_functions import make_date_utc


class StandardAgreementToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agreement

    date_from = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    date_until = make_date_utc(datetime.datetime(2024, 6, 15, 00))
    amount = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardResourceFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    status = factory.SubFactory(AgreedAgreementStatusFactory)
    costs = factory.SubFactory(StandardResourcePriceFactory)
    type = factory.SubFactory(StandardAgreementTypeFactory)


class StandardHumanResourceAgreementToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agreement

    date_from = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    date_until = make_date_utc(datetime.datetime(2024, 6, 15, 00))
    amount = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardHumanResourceFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    status = factory.SubFactory(AgreedAgreementStatusFactory)
    costs = factory.SubFactory(StandardResourcePriceFactory)
    type = factory.SubFactory(StandardAgreementTypeFactory)
