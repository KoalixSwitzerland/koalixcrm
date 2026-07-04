# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_supply import ProductSupply
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory

# Referenced by dotted string path (not a direct module-level import) to
# avoid a circular import: tests.factories.products.__init__ pulls in this
# module, and tests.factories.contacts.supplier_factory transitively pulls
# in tests.factories.contacts.__init__, which (via contact_factory ->
# core.workspace_factory -> core.__init__ -> product_type_factory) reaches
# back into tests.factories.products.__init__ before it has finished
# initializing. factory.SubFactory resolves a dotted string lazily at
# instantiation time, sidestepping the import-time cycle.
_SUPPLIER_FACTORY_PATH = "tests.factories.contacts.supplier_factory.StandardSupplierFactory"


class StandardProductSupplyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSupply
        django_get_or_create = ('product', 'supplier')

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    supplier = factory.SubFactory(_SUPPLIER_FACTORY_PATH)
    supplier_sku = "SUP-SKU-123456"
    lead_time_days = 14
    moq = "10.0000"
    purchase_price = "42.50"
    purchase_currency = None
