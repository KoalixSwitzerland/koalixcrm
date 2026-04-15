# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.delivery_note import DeliveryNote
from koalixcrm.contracts.factory.commercial_document_factory import StandardCommercialDocumentFactory


class StandardDeliveryNoteFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = DeliveryNote

    tracking_reference = "This is a tracking reference"
    status = "S"

