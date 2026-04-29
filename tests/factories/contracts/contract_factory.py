# -*- coding: utf-8 -*-

import factory

from koalixcrm.contracts.models.contract import Contract
from tests.factories.contacts.customer_factory import StandardCustomerFactory
from tests.factories.contacts.user_factory import StaffUserFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.djangoUserExtension.factory_template_set import (
    StandardTemplateSetFactory,
)


class StandardContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contract

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    staff = factory.SubFactory(StaffUserFactory)
    description = "This is the description to a test contract"
    buyer_party = factory.SubFactory(StandardCustomerFactory)
    default_currency = factory.SubFactory(StandardCurrencyFactory)
    default_template_set = factory.SubFactory(StandardTemplateSetFactory)
    date_of_creation = "2018-05-01"
    last_modification = "2018-05-03"
    last_modified_by = factory.SubFactory(StaffUserFactory)
