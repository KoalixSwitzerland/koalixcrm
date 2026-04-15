# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.sales_order import SalesOrder
from koalixcrm.contracts.factory.commercial_document_factory import StandardCommercialDocumentFactory


class StandardSalesOrderFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = SalesOrder


