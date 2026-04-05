# -*- coding: utf-8 -*-

import factory
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.crm.factory.supplier_factory import StandardSupplierFactory
from koalixcrm.contracts.factory.sales_document_factory import StandardSalesDocumentFactory


class StandardPurchaseOrderFactory(StandardSalesDocumentFactory):
    class Meta:
        model = PurchaseOrder

    supplier = factory.SubFactory(StandardSupplierFactory)
    status = "C"
