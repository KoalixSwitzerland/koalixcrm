# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.quote import Quote
from koalixcrm.contracts.factory.commercial_document_factory import StandardCommercialDocumentFactory


class StandardQuoteFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = Quote

    valid_until = "2018-05-20"
    status = "I"
