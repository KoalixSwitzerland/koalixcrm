# -*- coding: utf-8 -*-

import factory

from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.contacts.tests.factories.supplier_factory import StandardSupplierFactory
from koalixcrm.contracts.tests.factories.commercial_document_factory import (
    StandardCommercialDocumentFactory,
)


class StandardPurchaseOrderFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = PurchaseOrder

    supplier = factory.SubFactory(StandardSupplierFactory)
    status = "C"
