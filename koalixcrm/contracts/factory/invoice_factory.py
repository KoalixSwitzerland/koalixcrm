# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.factory.sales_document_factory import StandardSalesDocumentFactory


class StandardInvoiceFactory(StandardSalesDocumentFactory):
    class Meta:
        model = Invoice

    payable_until = "2018-05-20"
    payment_bank_reference = "This is a bank account reference"
    status = "C"
