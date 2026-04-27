# -*- coding: utf-8 -*-

import factory

from koalixcrm.contacts.models.address import Address
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory


class StandardPostalAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    street = "Main-street"
    number = "5"
    additional_address_line_1 = None
    additional_address_line_2 = None
    additional_address_line_3 = None
    zip_code = "8000"
    town = "Zürich"
    state = "ZH"
    country = "CH"
