# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import CustomerGroup


class StandardCustomerGroupFactory(factory.Factory):
    class Meta:
        model = CustomerGroup

    name = factory.Sequence(lambda n: "Customer Group #%s" % n)


