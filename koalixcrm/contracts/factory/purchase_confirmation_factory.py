# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.purchase_confirmation import PurchaseConfirmation
from koalixcrm.contracts.factory.sales_document_factory import StandardSalesDocumentFactory


class StandardPurchaseConfirmationFactory(StandardSalesDocumentFactory):
    class Meta:
        model = PurchaseConfirmation


