# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Supplier
from tests.factories.crm.contact_factory import StandardContactFactory


class StandardSupplierFactory(StandardContactFactory):
    class Meta:
        model = Supplier

    offers_shipment_to_customers = True
