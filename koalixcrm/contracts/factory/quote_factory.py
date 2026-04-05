# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.quote import Quote
from koalixcrm.contracts.factory.sales_document_factory import StandardSalesDocumentFactory


class StandardQuoteFactory(StandardSalesDocumentFactory):
    class Meta:
        model = Quote

    valid_until = "2018-05-20"
    status = "C"
