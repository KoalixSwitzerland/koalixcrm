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
from koalixcrm.crm.product.attribute import AttributeSet, OptionAttributeSet, Attribute, OptionAttribute
from koalixcrm.crm.contact.customer import Customer, OptionCustomer
from koalixcrm.crm.contact.supplier import Supplier, OptionSupplier
from koalixcrm.crm.contact.customergroup import CustomerGroup, OptionCustomerGroup
from koalixcrm.crm.contact.customerbillingcycle import CustomerBillingCycle, OptionCustomerBillingCycle
from koalixcrm.crm.contact.person import Person
from koalixcrm.crm.contact.contact import CallForContact, OptionCall, OptionPerson
from koalixcrm.crm.contact.data_import import ContactImportData
from koalixcrm.crm.forms import ImportDataContactForm

class ContactImportDataAdmin(admin.ModelAdmin):
    model = ContactImportData
    list_display = ('data_file', 'contact_type',)
    form = ImportDataContactForm
    group_fieldsets = True

    def get_actions(self, request):
        actions = super(ContactImportDataAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContactImportDataAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def __init__(self, *args, **kwargs):
        super(ContactImportDataAdmin, self).__init__(*args, **kwargs)
        #self.list_display_links = (None, )

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
admin.site.register(AttributeSet, OptionAttributeSet)
admin.site.register(Attribute, OptionAttribute)
admin.site.register(CallForContact, OptionCall)
admin.site.register(Visit, OptionVisit)
admin.site.register(Person, OptionPerson)

admin.site.register(ContactImportData, ContactImportDataAdmin)
