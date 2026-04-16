# -*- coding: utf-8 -*-

import factory
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from tests.factories.contacts.supplier_factory import StandardSupplierFactory
from tests.factories.contracts.commercial_document_factory import StandardCommercialDocumentFactory


class StandardPurchaseOrderFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = PurchaseOrder

    supplier = factory.SubFactory(StandardSupplierFactory)
    status = "C"
