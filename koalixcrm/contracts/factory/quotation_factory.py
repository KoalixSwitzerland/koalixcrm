# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.contracts.factory.commercial_document_factory import StandardCommercialDocumentFactory


class StandardQuotationFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = Quotation

    valid_until = "2018-05-20"
    status = "I"
