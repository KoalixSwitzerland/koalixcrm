# -*- coding: utf-8 -*-

import factory

from koalixcrm.djangoUserExtension.models import UserExtension
from tests.factories.contacts.user_factory import StaffUserFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.djangoUserExtension.factory_template_set import (
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
