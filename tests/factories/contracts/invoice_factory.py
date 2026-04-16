# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.invoice import Invoice
from tests.factories.contracts.commercial_document_factory import StandardCommercialDocumentFactory


class StandardInvoiceFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = Invoice

    payable_until = "2018-05-20"
    payment_bank_reference = "This is a bank account reference"
    status = "C"
