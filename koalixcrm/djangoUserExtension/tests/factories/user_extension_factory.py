# -*- coding: utf-8 -*-

import factory

from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.contacts.tests.factories.user_factory import StaffUserFactory
from koalixcrm.core.tests.factories.currency_factory import StandardCurrencyFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.djangoUserExtension.tests.factories.template_set_factory import (
    StandardTemplateSetFactory,
)


class StandardUserExtensionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserExtension
        django_get_or_create = ('user',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    user = factory.SubFactory(StaffUserFactory)
    default_template_set = factory.SubFactory(StandardTemplateSetFactory)
    default_currency = factory.SubFactory(StandardCurrencyFactory)
