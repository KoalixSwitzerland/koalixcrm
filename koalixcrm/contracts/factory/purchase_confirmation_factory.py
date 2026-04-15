# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.purchase_confirmation import PurchaseConfirmation
from koalixcrm.contracts.factory.commercial_document_factory import StandardCommercialDocumentFactory


class StandardPurchaseConfirmationFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = PurchaseConfirmation


