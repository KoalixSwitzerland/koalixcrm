# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Contact
from koalixcrm.crm.factories.factory_user import StaffUserFactory


class StandardContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact
        django_get_or_create = ('name',)

    name = "John Smith"
    date_of_creation = "2018-05-01"
    last_modification = "2018-05-03"
    last_modified_by = factory.SubFactory(StaffUserFactory)
