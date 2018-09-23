# -*- coding: utf-8 -*-

from koalixcrm.crm.models import Invoice
from koalixcrm.crm.factories.factory_sales_document import StandardSalesDocumentFactory


class StandardInvoiceFactory(StandardSalesDocumentFactory):
    class Meta:
        model = Invoice

    payable_until = "2018-05-20"
    payment_bank_reference = "This is a bank account reference"
    status = "C"
