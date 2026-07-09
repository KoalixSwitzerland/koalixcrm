# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.customer_group_transform import CustomerGroupTransform
from koalixcrm.contacts.tests.factories.customer_group_factory import (
    AdvancedCustomerGroupFactory,
    StandardCustomerGroupFactory,
)
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class StandardCustomerGroupTransformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerGroupTransform

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    from_party_group = factory.SubFactory(AdvancedCustomerGroupFactory)
    to_party_group = factory.SubFactory(StandardCustomerGroupFactory)
    product_type = factory.SubFactory(StandardProductTypeFactory)
    factor = "10"
