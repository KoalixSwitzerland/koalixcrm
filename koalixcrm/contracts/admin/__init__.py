# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.contracts.models.contract import Contract
from koalixcrm.contracts.models.quote import Quote
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.models.purchase_confirmation import PurchaseConfirmation
from koalixcrm.contracts.models.delivery_note import DeliveryNote
from koalixcrm.contracts.models.payment_reminder import PaymentReminder
from koalixcrm.contracts.models.purchase_order import PurchaseOrder

from koalixcrm.contracts.admin.contract_admin import OptionContract  # noqa: F401
from koalixcrm.contracts.admin.quote_admin import OptionQuote, InlineQuote  # noqa: F401
from koalixcrm.contracts.admin.invoice_admin import OptionInvoice, InlineInvoice  # noqa: F401
from koalixcrm.contracts.admin.purchase_confirmation_admin import OptionPurchaseConfirmation  # noqa: F401
from koalixcrm.contracts.admin.delivery_note_admin import OptionDeliveryNote  # noqa: F401
from koalixcrm.contracts.admin.payment_reminder_admin import OptionPaymentReminder  # noqa: F401
from koalixcrm.contracts.admin.purchase_order_admin import OptionPurchaseOrder  # noqa: F401
from koalixcrm.contracts.admin.sales_document_admin import OptionSalesDocument  # noqa: F401
from koalixcrm.contracts.admin.sales_document_position_admin import SalesDocumentInlinePosition  # noqa: F401

admin.site.register(Contract, OptionContract)
admin.site.register(Quote, OptionQuote)
admin.site.register(PurchaseConfirmation, OptionPurchaseConfirmation)
admin.site.register(DeliveryNote, OptionDeliveryNote)
admin.site.register(Invoice, OptionInvoice)
admin.site.register(PaymentReminder, OptionPaymentReminder)
admin.site.register(PurchaseOrder, OptionPurchaseOrder)
