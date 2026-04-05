# -*- coding: utf-8 -*-

import factory
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.crm.factory.user_factory import StaffUserFactory
from koalixcrm.products.factory.currency_factory import StandardCurrencyFactory
from koalixcrm.djangoUserExtension.factories.factory_template_set import StandardTemplateSetFactory


class StandardUserExtensionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserExtension
        django_get_or_create = ('user',)

    user = factory.SubFactory(StaffUserFactory)
    default_template_set = factory.SubFactory(StandardTemplateSetFactory)
    default_currency = factory.SubFactory(StandardCurrencyFactory)
