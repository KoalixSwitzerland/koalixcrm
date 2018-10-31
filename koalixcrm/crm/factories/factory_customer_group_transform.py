# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.product.customer_group_transform import CustomerGroupTransform
from koalixcrm.crm.factories.factory_product_type import StandardProductTypeFactory
from koalixcrm.crm.factories.factory_customer_group import AdvancedCustomerGroupFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory


class StandardCustomerGroupTransformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerGroupTransform
    from_customer_group = factory.SubFactory(AdvancedCustomerGroupFactory)
    to_customer_group = factory.SubFactory(StandardCustomerGroupFactory)
    product_type = factory.SubFactory(StandardProductTypeFactory)
    factor = "10"
