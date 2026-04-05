# -*- coding: utf-8 -*-

import factory
from koalixcrm.contracts.models.contract import Contract
from koalixcrm.crm.factory.user_factory import StaffUserFactory
from koalixcrm.crm.factory.customer_factory import StandardCustomerFactory
from koalixcrm.products.factory.currency_factory import StandardCurrencyFactory
from koalixcrm.djangoUserExtension.factories.factory_template_set import StandardTemplateSetFactory


class StandardContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contract

    staff = factory.SubFactory(StaffUserFactory)
    description = "This is the description to a test contract"
    default_customer = factory.SubFactory(StandardCustomerFactory)
    default_currency = factory.SubFactory(StandardCurrencyFactory)
    default_template_set = factory.SubFactory(StandardTemplateSetFactory)
    date_of_creation = "2018-05-01"
    last_modification = "2018-05-03"
    last_modified_by = factory.SubFactory(StaffUserFactory)
