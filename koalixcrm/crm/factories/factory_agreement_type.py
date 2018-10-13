# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import AgreementType


class StandardAgreementTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgreementType

    title = 'This is a test Agreement Type'
    description = "This is a description of such a Agreement Type"
