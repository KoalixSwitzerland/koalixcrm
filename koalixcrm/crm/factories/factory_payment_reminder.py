# -*- coding: utf-8 -*-

from koalixcrm.crm.models import PaymentReminder
from koalixcrm.crm.factories.factory_sales_document import StandardSalesDocumentFactory


class StandardPaymentReminderFactory(StandardSalesDocumentFactory):
    class Meta:
        model = PaymentReminder

    payable_until = "2018-05-20"
    payment_bank_reference = "This is a bank account reference"
    iteration_number = "1"
    status = "C"
