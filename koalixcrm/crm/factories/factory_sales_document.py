# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import SalesDocument
from koalixcrm.crm.factories.factory_user import StaffUserFactory
from koalixcrm.crm.factories.factory_contract import StandardContractFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_supplier import StandardSupplierFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.djangoUserExtension.factories import StandardDefaultTemplateSet


class StandardSalesDocumentFactory(factory.Factory):
    class Meta:
        model = SalesDocument

    contract = factory.SubFactory(StandardContractFactory)
    external_reference = "This is an external Reference"
    discount = "10.10"
    description = "This is the description of a sales document"
    last_pricing_date = "2018-05-01"
    last_calculated_price = "220.00"
    last_calculated_tax = "10.00"
    customer = factory.SubFactory(StandardCustomerFactory)
    staff = factory.SubFactory(StaffUserFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    date_of_creation = "2018-05-01"
    custom_date_field = "2018-05-20"
    last_modification = "2018-05-25"
    last_modified_by = factory.SubFactory(StaffUserFactory)
    template_set = factory.SubFactory(StandardDefaultTemplateSet)
    derived_from_sales_document = None
    last_print_date = "2018-05-26"

