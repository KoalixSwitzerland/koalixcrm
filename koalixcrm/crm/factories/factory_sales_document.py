# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.crm.models import SalesDocument
from koalixcrm.crm.factories.factory_user import StaffUserFactory
from koalixcrm.crm.factories.factory_contract import StandardContractFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.djangoUserExtension.factories.factory_document_template import StandardQuoteTemplateFactory


class StandardSalesDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SalesDocument

    contract = factory.SubFactory(StandardContractFactory)
    external_reference = "This is an external Reference"
    discount = "0"
    description = "This is the description of a sales document"
    last_pricing_date = make_date_utc(datetime.datetime(2018, 5, 1, 00))
    last_calculated_price = "220.00"
    last_calculated_tax = "10.00"
    customer = factory.SubFactory(StandardCustomerFactory)
    staff = factory.SubFactory(StaffUserFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    date_of_creation = make_date_utc(datetime.datetime(2018, 5, 1, 00))
    custom_date_field = make_date_utc(datetime.datetime(2018, 5, 20, 00))
    last_modification = make_date_utc(datetime.datetime(2018, 5, 25, 00))
    last_modified_by = factory.SubFactory(StaffUserFactory)
    template_set = factory.SubFactory(StandardQuoteTemplateFactory)
    derived_from_sales_document = None
    last_print_date = make_date_utc(datetime.datetime(2018, 5, 26, 00))

