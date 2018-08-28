# -*- coding: utf-8 -*-

from koalixcrm.crm.models import Quote
from koalixcrm.crm.factories.factory_sales_document import StandardSalesDocumentFactory


class StandardQuoteFactory(StandardSalesDocumentFactory):
    class Meta:
        model = Quote

    valid_until = "2018-05-20"
    status = "C"
