# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.quotation import Quotation
from tests.factories.contracts.commercial_document_factory import StandardCommercialDocumentFactory


class StandardQuotationFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = Quotation

    valid_until = "2018-05-20"
    status = "I"
