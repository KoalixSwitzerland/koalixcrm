# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.despatch_advice import DespatchAdvice
from tests.factories.contracts.commercial_document_factory import (
    StandardCommercialDocumentFactory,
)


class StandardDespatchAdviceFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = DespatchAdvice

    tracking_reference = "This is a tracking reference"
    status = "S"

