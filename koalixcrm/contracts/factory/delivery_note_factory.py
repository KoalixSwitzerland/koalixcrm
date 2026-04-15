# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.delivery_note import DeliveryNote
from koalixcrm.contracts.factory.sales_document_factory import StandardSalesDocumentFactory


class StandardDeliveryNoteFactory(StandardSalesDocumentFactory):
    class Meta:
        model = DeliveryNote

    tracking_reference = "This is a tracking reference"
    status = "S"

