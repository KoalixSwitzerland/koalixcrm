# -*- coding: utf-8 -*-

from koalixcrm.crm.models import DeliveryNote
from koalixcrm.crm.factories.factory_sales_document import StandardSalesDocumentFactory


class StandardDeliveryNoteFactory(StandardSalesDocumentFactory):
    class Meta:
        model = DeliveryNote

    tracking_reference = "This is a tracking reference"
    status = "S"

