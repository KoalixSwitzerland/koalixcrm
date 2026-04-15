# -*- coding: utf-8 -*-

import factory
from koalixcrm.products.models.customer_group_transform import CustomerGroupTransform
from tests.factories.products.product_type_factory import StandardProductTypeFactory
from tests.factories.crm.customer_group_factory import AdvancedCustomerGroupFactory
from tests.factories.crm.customer_group_factory import StandardCustomerGroupFactory


class StandardCustomerGroupTransformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerGroupTransform
    from_customer_group = factory.SubFactory(AdvancedCustomerGroupFactory)
    to_customer_group = factory.SubFactory(StandardCustomerGroupFactory)
    product_type = factory.SubFactory(StandardProductTypeFactory)
    factor = "10"
