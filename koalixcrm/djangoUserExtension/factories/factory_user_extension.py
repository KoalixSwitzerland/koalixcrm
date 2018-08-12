# -*- coding: utf-8 -*-

import factory
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.crm.factories.factory_user import StaffUserFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.djangoUserExtension.factories.factory_template_set import StandardTemplateSetFactory


class StandardUserExtensionFactory(factory.Factory):
    class Meta:
        model = UserExtension

    user = factory.SubFactory(StaffUserFactory)
    default_template_set = factory.SubFactory(StandardTemplateSetFactory)
    default_currency = factory.SubFactory(StandardCurrencyFactory)
