# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.global_support_functions import make_date_utc
from tests.factories.contacts.customer_factory import StandardCustomerFactory
from tests.factories.contacts.user_factory import StaffUserFactory
from tests.factories.contracts.contract_factory import StandardContractFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.djangoUserExtension.factory_document_template import (
    StandardQuotationTemplateFactory,
)


class StandardCommercialDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommercialDocument

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    contract = factory.SubFactory(StandardContractFactory)
    party_reference = "This is a party Reference"
    discount = "0"
    description = "This is the description of a commercial document"
    last_pricing_date = make_date_utc(datetime.datetime(2018, 5, 1, 00))
    last_calculated_price = "220.00"
    last_calculated_tax = "10.00"
    party = factory.SubFactory(StandardCustomerFactory)
    staff = factory.SubFactory(StaffUserFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    date_of_creation = make_date_utc(datetime.datetime(2018, 5, 1, 00))
    custom_date_field = make_date_utc(datetime.datetime(2018, 5, 20, 00))
    last_modification = make_date_utc(datetime.datetime(2018, 5, 25, 00))
    last_modified_by = factory.SubFactory(StaffUserFactory)
    template_set = factory.SubFactory(StandardQuotationTemplateFactory)
    derived_from_commercial_document = None
    last_print_date = make_date_utc(datetime.datetime(2018, 5, 26, 00))
