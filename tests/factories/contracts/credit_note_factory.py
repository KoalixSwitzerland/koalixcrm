# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.credit_note import CreditNote
from tests.factories.contracts.commercial_document_factory import StandardCommercialDocumentFactory


class StandardCreditNoteFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = CreditNote

    corrects_invoice = None
    status = "C"
    issue_date = "2018-05-20"
    reason = "Test credit note reason"
