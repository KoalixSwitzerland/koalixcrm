# -*- coding: utf-8 -*-

from koalixcrm.crm.models import PurchaseConfirmation
from koalixcrm.crm.factories.factory_sales_document import StandardSalesDocumentFactory


class StandardPurchaseConfirmationFactory(StandardSalesDocumentFactory):
    class Meta:
        model = PurchaseConfirmation


