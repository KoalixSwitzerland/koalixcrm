# -*- coding: utf-8 -*-

from django.contrib import admin
from koalixcrm.crm.documents.quote import Quote, OptionQuote
from koalixcrm.crm.documents.purchaseconfirmation import PurchaseConfirmation, OptionPurchaseConfirmation
from koalixcrm.crm.documents.deliverynote import DeliveryNote, OptionDeliveryNote
from koalixcrm.crm.documents.invoice import Invoice, OptionInvoice
from koalixcrm.crm.documents.paymentreminder import PaymentReminder, OptionPaymentReminder
from koalixcrm.crm.documents.purchaseorder import PurchaseOrder, OptionPurchaseOrder
from koalixcrm.crm.documents.contract import Contract, OptionContract
from koalixcrm.crm.documents.activity import Call
from koalixcrm.crm.documents.visit import Visit, OptionVisit
from koalixcrm.crm.product.tax import Tax, OptionTax
from koalixcrm.crm.product.unit import Unit, OptionUnit
from koalixcrm.crm.product.product import Product, OptionProduct
from koalixcrm.crm.product.currency import Currency, OptionCurrency
from koalixcrm.crm.contact.customer import Customer, OptionCustomer
from koalixcrm.crm.contact.supplier import Supplier, OptionSupplier
from koalixcrm.crm.contact.customergroup import CustomerGroup, OptionCustomerGroup
from koalixcrm.crm.contact.customerbillingcycle import CustomerBillingCycle, OptionCustomerBillingCycle
from koalixcrm.crm.contact.person import Person
from koalixcrm.crm.contact.contact import CallForContact, OptionCall, OptionPerson

admin.site.register(Customer, OptionCustomer)
admin.site.register(CustomerGroup, OptionCustomerGroup)
admin.site.register(CustomerBillingCycle, OptionCustomerBillingCycle)
admin.site.register(Supplier, OptionSupplier)

admin.site.register(Contract, OptionContract)
admin.site.register(Quote, OptionQuote)
admin.site.register(PurchaseConfirmation, OptionPurchaseConfirmation)
admin.site.register(DeliveryNote, OptionDeliveryNote)
admin.site.register(Invoice, OptionInvoice)
admin.site.register(PaymentReminder, OptionPaymentReminder)
admin.site.register(PurchaseOrder, OptionPurchaseOrder)

admin.site.register(Unit, OptionUnit)
admin.site.register(Currency, OptionCurrency)
admin.site.register(Tax, OptionTax)
admin.site.register(Product, OptionProduct)
admin.site.register(CallForContact, OptionCall)
admin.site.register(Visit, OptionVisit)
admin.site.register(Person, OptionPerson)
