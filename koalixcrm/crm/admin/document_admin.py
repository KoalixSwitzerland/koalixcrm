# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.contract_object_management.models.quote import Quote, OptionQuote
from koalixcrm.contract_object_management.models.purchase_confirmation import PurchaseConfirmation, OptionPurchaseConfirmation
from koalixcrm.contract_object_management.models.delivery_note import DeliveryNote, OptionDeliveryNote
from koalixcrm.contract_object_management.models.invoice import Invoice, OptionInvoice
from koalixcrm.contract_object_management.models.payment_reminder import PaymentReminder, OptionPaymentReminder
from koalixcrm.contract_object_management.models.purchase_order import PurchaseOrder, OptionPurchaseOrder
from koalixcrm.contract_object_management.models.contract import Contract, OptionContract

admin.site.register(Contract, OptionContract)
admin.site.register(Quote, OptionQuote)
admin.site.register(PurchaseConfirmation, OptionPurchaseConfirmation)
admin.site.register(DeliveryNote, OptionDeliveryNote)
admin.site.register(Invoice, OptionInvoice)
admin.site.register(PaymentReminder, OptionPaymentReminder)
admin.site.register(PurchaseOrder, OptionPurchaseOrder)
