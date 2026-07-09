# -*- coding: utf-8 -*-

from koalixcrm.contracts.models.payment_reminder import PaymentReminder
from koalixcrm.contracts.tests.factories.commercial_document_factory import (
    StandardCommercialDocumentFactory,
)


class StandardPaymentReminderFactory(StandardCommercialDocumentFactory):
    class Meta:
        model = PaymentReminder

    payable_until = "2018-05-20"
    payment_bank_reference = "This is a bank account reference"
    iteration_number = "1"
    status = "C"
