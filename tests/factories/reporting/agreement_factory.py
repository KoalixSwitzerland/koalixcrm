# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.reporting.models.agreement import Agreement
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.reporting.agreement_status_factory import (
    AgreedAgreementStatusFactory,
)
from tests.factories.reporting.agreement_type_factory import (
    StandardAgreementTypeFactory,
)
from tests.factories.reporting.human_resource_factory import (
    StandardHumanResourceFactory,
)
from tests.factories.reporting.resource_factory import StandardResourceFactory
from tests.factories.reporting.resource_price_factory import (
    StandardResourcePriceFactory,
)
from tests.factories.reporting.task_factory import StandardTaskFactory


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
