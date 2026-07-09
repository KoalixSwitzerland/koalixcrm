# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.reporting.models.agreement import Agreement
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.reporting.tests.factories.agreement_status_factory import (
    AgreedAgreementStatusFactory,
)
from koalixcrm.reporting.tests.factories.agreement_type_factory import (
    StandardAgreementTypeFactory,
)
from koalixcrm.reporting.tests.factories.human_resource_factory import (
    StandardHumanResourceFactory,
)
from koalixcrm.reporting.tests.factories.resource_factory import StandardResourceFactory
from koalixcrm.reporting.tests.factories.resource_price_factory import (
    StandardResourcePriceFactory,
)
from koalixcrm.reporting.tests.factories.task_factory import StandardTaskFactory


class StandardAgreementToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agreement

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
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

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    date_from = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    date_until = make_date_utc(datetime.datetime(2024, 6, 15, 00))
    amount = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardHumanResourceFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    status = factory.SubFactory(AgreedAgreementStatusFactory)
    costs = factory.SubFactory(StandardResourcePriceFactory)
    type = factory.SubFactory(StandardAgreementTypeFactory)
