# -*- coding: utf-8 -*-

import factory
from koalixcrm.contacts.models import PostalAddress
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory


class StandardPostalAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostalAddress

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    prefix = "M"
    name = "Smith"
    pre_name = "John"
    address_line_1 = "Main-street 5"
    address_line_2 = None
    address_line_3 = None
    address_line_4 = None
    zip_code = 8000
    town = "Zürich"
    state = "ZH"
    country = "CH"
