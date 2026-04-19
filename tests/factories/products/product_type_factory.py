# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.products.models.product_type import ProductType
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.contacts.user_factory import StaffUserFactory
from tests.factories.core.tax_factory import StandardTaxFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.global_support_functions import make_date_utc


class StandardProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        django_get_or_create = ('product_type_identifier',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    title = "This is a test Product"
    description = "This is a test Product"
    product_type_identifier = "123456"
    default_unit = factory.SubFactory(StandardUnitFactory)
    date_of_creation = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    last_modification = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    last_modified_by = factory.SubFactory(StaffUserFactory)
    tax = factory.SubFactory(StandardTaxFactory)
