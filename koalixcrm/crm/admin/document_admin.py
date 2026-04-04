# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.crm.documents.quote import Quote, OptionQuote
from koalixcrm.crm.documents.purchase_confirmation import PurchaseConfirmation, OptionPurchaseConfirmation
from koalixcrm.crm.documents.delivery_note import DeliveryNote, OptionDeliveryNote
from koalixcrm.crm.documents.invoice import Invoice, OptionInvoice
from koalixcrm.crm.documents.payment_reminder import PaymentReminder, OptionPaymentReminder
from koalixcrm.crm.documents.purchase_order import PurchaseOrder, OptionPurchaseOrder
from koalixcrm.crm.documents.contract import Contract, OptionContract

admin.site.register(Contract, OptionContract)
admin.site.register(Quote, OptionQuote)
admin.site.register(PurchaseConfirmation, OptionPurchaseConfirmation)
admin.site.register(DeliveryNote, OptionDeliveryNote)
admin.site.register(Invoice, OptionInvoice)
admin.site.register(PaymentReminder, OptionPaymentReminder)
admin.site.register(PurchaseOrder, OptionPurchaseOrder)
