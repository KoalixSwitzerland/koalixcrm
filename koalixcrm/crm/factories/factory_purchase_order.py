# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import PurchaseOrder
from koalixcrm.crm.factories.factory_supplier import StandardSupplierFactory
from koalixcrm.crm.factories.factory_sales_document import StandardSalesDocumentFactory


class StandardPurchaseOrderFactory(StandardSalesDocumentFactory):
    class Meta:
        model = PurchaseOrder

    supplier = factory.SubFactory(StandardSupplierFactory)
    status = "C"
