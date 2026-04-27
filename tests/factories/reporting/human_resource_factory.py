# -*- coding: utf-8 -*-

import factory

from koalixcrm.reporting.models.human_resource import HumanResource
from tests.factories.djangoUserExtension.factory_user_extension import (
    StandardUserExtensionFactory,
)
from tests.factories.reporting.resource_manager_factory import (
    StandardResourceManagerFactory,
)
from tests.factories.reporting.resource_type_factory import StandardResourceTypeFactory


class StandardHumanResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HumanResource

    user = factory.SubFactory(StandardUserExtensionFactory)
    resource_type = factory.SubFactory(StandardResourceTypeFactory)
    resource_manager = factory.SubFactory(StandardResourceManagerFactory)
