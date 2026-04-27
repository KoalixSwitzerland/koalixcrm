# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.customer_group_transform import CustomerGroupTransform
from tests.factories.contacts.customer_group_factory import (
    AdvancedCustomerGroupFactory,
    StandardCustomerGroupFactory,
)
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class StandardCustomerGroupTransformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerGroupTransform

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    from_party_group = factory.SubFactory(AdvancedCustomerGroupFactory)
    to_party_group = factory.SubFactory(StandardCustomerGroupFactory)
    product_type = factory.SubFactory(StandardProductTypeFactory)
    factor = "10"
