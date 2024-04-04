# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.crm.models import Agreement
from koalixcrm.crm.factories.factory_resource import StandardResourceFactory
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory
from koalixcrm.crm.factories.factory_resource_price import StandardResourcePriceFactory
from koalixcrm.crm.factories.factory_agreement_type import StandardAgreementTypeFactory
from koalixcrm.crm.factories.factory_agreement_status import AgreedAgreementStatusFactory
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
